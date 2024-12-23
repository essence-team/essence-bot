from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

digest_freq_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Еженедельно", callback_data="weekly")],
        [InlineKeyboardButton(text="Ежемесячно", callback_data="monthly")],
    ]
)
