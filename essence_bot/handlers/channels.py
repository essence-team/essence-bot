import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from handlers.utils import parse_and_normalize_links
from keyboards.channels import get_channel_add_kb, get_channel_remove_kb
from services.essence_backend import EssenceBackendAPI
from states.states import ChannelStates

channel_router = Router(name="channel_router")


@channel_router.message(F.text == "Добавить каналы")
async def add_channels_prompt(message: Message, state: FSMContext, logger: logging.Logger):
    user_id = str(message.from_user.id)

    logger.info(f"User {user_id} requested to add channels.")

    # Переход в состояние ожидания ввода каналов
    await state.set_state(ChannelStates.waiting_for_channels)
    await message.answer("Введите ссылки на ваши каналы через пробел или каждый в отдельной строке:")


@channel_router.message(ChannelStates.waiting_for_channels, F.text)
async def process_channels_input(
    message: Message,
    essence_api: EssenceBackendAPI,
    state: FSMContext,
    logger: logging.Logger,
):
    user_id = str(message.from_user.id)
    text = message.text.strip()

    logger.info(f"User {user_id} provided channel links: {text}")

    channel_links = parse_and_normalize_links(text)

    result = await essence_api.add_channels(user_id=user_id, channel_links=channel_links)

    invalid_links = [channel.channel_link for channel in result if not channel.exists]
    if not invalid_links:
        await message.answer("Ваши каналы успешно добавлены!")
        await state.clear()
        return

    valid_links = [channel.channel_link for channel in result if channel.exists]

    logger.info(f"Added channels for user {user_id}: {valid_links}")
    await message.answer(f"C этими каналами возникли проблемы: {invalid_links}")

    await state.clear()


@channel_router.message(F.text == "Мои каналы")
async def list_user_channels(message: Message, essence_api: EssenceBackendAPI, logger: logging.Logger):
    user_id = str(message.from_user.id)
    logger.info(f"User {user_id} requested to list their channels.")

    channels = await essence_api.get_user_channels(user_id=user_id)
    if not channels:
        await message.answer("У вас нет добавленных каналов.")
        return

    for channel in channels:
        keyboard = get_channel_remove_kb(channel.channel_link)
        await message.answer(f"t.me/{channel.channel_link}", reply_markup=keyboard)


@channel_router.callback_query(F.data.startswith("delete_channel:"))
async def delete_channel_callback(
    callback_query: CallbackQuery,
    essence_api: EssenceBackendAPI,
    logger: logging.Logger,
):
    user_id = str(callback_query.from_user.id)
    channel_link = callback_query.data.split(":", 1)[1]

    logger.info(f"User {user_id} requested to delete channel: {channel_link}")

    try:
        await essence_api.remove_channels(user_id=user_id, channel_links=[channel_link])
    except Exception:
        await callback_query.answer("Не удалось удалить канал.")

    keyboard = get_channel_add_kb(channel_link)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer("Канал удален.")


@channel_router.callback_query(F.data.startswith("restore_channel:"))
async def restore_channel_callback(
    callback_query: CallbackQuery,
    essence_api: EssenceBackendAPI,
    logger: logging.Logger,
):
    user_id = str(callback_query.from_user.id)
    channel_link = callback_query.data.split(":", 1)[1]

    logger.info(f"User {user_id} requested to restore channel: {channel_link}")

    try:
        await essence_api.add_channels(user_id=user_id, channel_links=[channel_link])
    except Exception:
        await callback_query.answer("Не удалось восстановить канал.")

    keyboard = get_channel_remove_kb(channel_link)
    await callback_query.message.edit_reply_markup(reply_markup=keyboard)
    await callback_query.answer("Канал восстановлен.")
