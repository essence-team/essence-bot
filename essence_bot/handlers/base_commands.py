import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import main_kb
from messages import PARSE_MODE_MARKDOWN, CommandsMessages
from services.essence_backend import EssenceBackendAPI

base_commands_router = Router(name="base_commands_router")


@base_commands_router.message(Command("start"))
async def start_handler(message: Message, essence_api: EssenceBackendAPI, logger: logging):
    user_id = str(message.from_user.id)
    user = await essence_api.get_user(user_id=user_id)

    if user is not None:
        await message.answer(
            CommandsMessages.COMEBACK_REGISTERED_USER.format(
                user_first_name=message.from_user.first_name,
            ),
            reply_markup=main_kb,
        )
    else:
        await essence_api.add_user(user_id=user_id, username=message.from_user.username)
        await essence_api.subscribe_user(payment_id=f"demo_{user_id}", user_id=user_id, days_cnt=7)
        await message.answer(CommandsMessages.START)

        await message.reply(
            text="Для вас активирована пробная подписка на 7 дней.",
            reply_markup=main_kb,
        )

    logger.info(
        "User use /start command.",
        extra={
            "user_id": message.from_user.id,
            "command": "start",
            "user_status": "comeback" if user else "new_user",
        },
    )


@base_commands_router.message(Command("help"))
async def help_handler(message: Message, logger: logging.Logger):
    await message.answer(CommandsMessages.HELP_MESSAGE)
    logger.info(
        "User use /help command.",
        extra={
            "user_id": message.from_user.id,
            "command": "help",
        },
    )


@base_commands_router.message(Command("feedback"))
async def feedback_handler(message: Message, logger: logging.Logger):
    await message.answer(
        CommandsMessages.FEEDBACK_MESSAGE,
        parse_mode=PARSE_MODE_MARKDOWN,
        disable_web_page_preview=True,
    )
    logger.info(
        "User use /feedback command.",
        extra={
            "user_id": message.from_user.id,
            "command": "help",
        },
    )
