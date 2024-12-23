from datetime import datetime, timedelta

from aiogram import BaseMiddleware, types
from aiogram.dispatcher.event.bases import CancelHandler
from messages import AntiFloodMessages


class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, limit=1):
        super().__init__()
        self.limit = limit
        self.last_message_time = {}

    async def __call__(self, handler, event: types.Message, data: dict):
        user_id = event.from_user.id

        # Получаем текущее время и последний отправленный пользователем запрос
        current_time = datetime.now()
        last_time = self.last_message_time.get(user_id)

        # Проверяем, если запрос был недавно и попадает под лимит времени
        if last_time and current_time - last_time < timedelta(seconds=self.limit):
            await event.answer(AntiFloodMessages.TOO_MANY_MESSAGES.format(seconds=self.limit))
            raise CancelHandler()  # Прерываем обработку сообщения

        # Обновляем время последнего сообщения пользователя
        self.last_message_time[user_id] = current_time
        return await handler(event, data)
