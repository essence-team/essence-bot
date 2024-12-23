import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from keyboards.digest_params import digest_freq_kb
from services.essence_backend import EssenceBackendAPI
from states.states import DigestParamsStates

digest_params_router = Router(name="digest_params_router")


@digest_params_router.message(F.text == "Изменить частоту дайджеста")
async def change_digest_params(message: Message, state: FSMContext, logger: logging.Logger):
    await message.answer("Выберите частоту дайджеста:", reply_markup=digest_freq_kb)
    await state.set_state(DigestParamsStates.waiting_for_freq)


@digest_params_router.callback_query(F.data.in_({"weekly", "monthly"}))
async def set_digest_frequency(callback_query: CallbackQuery, state: FSMContext):
    frequency = callback_query.data
    await state.update_data(digest_frequency=frequency)
    await callback_query.message.answer(
        "Введите час, в который вы хотите получать рассылку, например 18. Делаем рассылку в течение 6-24 часов."
    )
    await state.set_state(DigestParamsStates.waiting_for_hour)


@digest_params_router.message(DigestParamsStates.waiting_for_hour)
async def set_digest_hour(message: Message, state: FSMContext, essence_api: EssenceBackendAPI):
    hour = message.text
    if not hour.isdigit() or not (0 <= int(hour) <= 23):
        await message.answer("Пожалуйста, введите корректное значение часа (6-24).")
        return

    data = await state.get_data()
    frequency = data.get("digest_frequency")

    # Отправляем частоту и время на бэкенд
    user_id = str(message.from_user.id)
    await essence_api.set_digest_params(user_id, frequency, int(hour))

    await message.answer(f"Частота дайджеста установлена на {frequency}, время - {hour}:00")
    await state.clear()
