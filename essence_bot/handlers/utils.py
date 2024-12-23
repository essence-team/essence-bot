import asyncio
import re
from functools import wraps
from typing import List

from aiogram import types


def typing_action(func):
    @wraps(func)
    async def wrapper(message: types.Message, *args, **kwargs):
        async def send_typing_action(chat_id: int):
            bot = kwargs["bot"]
            while True:
                await bot.send_chat_action(chat_id, action="typing")
                await asyncio.sleep(5)

        typing_task = asyncio.create_task(send_typing_action(message.chat.id))
        try:
            result = await func(message, *args, **kwargs)
        finally:
            typing_task.cancel()
        return result

    return wrapper


def parse_and_normalize_links(text: str) -> List[str]:
    """
    Парсит текст, извлекает ссылки на Telegram каналы'
    """
    pattern = r"\b(?:https?:\/\/)?(?:t\.me\/|@)?\w+\b"
    matches = re.findall(pattern, text)
    unique_usernames = list(set(matches))

    return unique_usernames
