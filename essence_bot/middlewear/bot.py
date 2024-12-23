from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject


class BotMiddleware(BaseMiddleware):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    async def __call__(self, handler, event: TelegramObject, data: dict):
        data["bot"] = self.bot
        return await handler(event, data)
