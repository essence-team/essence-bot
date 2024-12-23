from dataclasses import dataclass


@dataclass
class CommandsMessages:
    START = "Привет! Я бот Essence, буду формировать дайджесты по каналам за которыми ты следишь! 🌟\n"

    COMEBACK_REGISTERED_USER = "С возвращением, {user_first_name}! 🌟\n"

    HELP_MESSAGE = "Здесь будет текст помощи по использованию бота.\n"

    FEEDBACK_MESSAGE = "Здесь должно быть сообщение о том, что пользователь может оставить свой отзыв и пожелания.\n"
