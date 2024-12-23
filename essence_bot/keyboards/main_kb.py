from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Получить дайджест")],
        [KeyboardButton(text="Добавить каналы"), KeyboardButton(text="Мои каналы")],
        [KeyboardButton(text="Подписка"), KeyboardButton(text="Изменить частоту дайджеста")],
        [KeyboardButton(text="Помощь")],
    ],
    resize_keyboard=True,
)
