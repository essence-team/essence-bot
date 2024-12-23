from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject


class LoggerMiddleware(BaseMiddleware):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["logger"] = self.logger
        return await handler(event, data)
