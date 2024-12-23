from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_channel_remove_kb(channel_link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="❌",
                    callback_data=f"delete_channel:{channel_link}",
                ),
            ]
        ]
    )
    return kb


def get_channel_add_kb(channel_link: str) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="↩️",
                    callback_data=f"restore_channel:{channel_link}",
                ),
            ]
        ]
    )
    return kb
