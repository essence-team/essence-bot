from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject


class EssenceAPIMiddleware(BaseMiddleware):
    def __init__(self, essence_api):
        super().__init__()
        self.essence_api = essence_api

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["essence_api"] = self.essence_api
        return await handler(event, data)
