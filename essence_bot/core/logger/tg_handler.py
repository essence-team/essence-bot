import asyncio
import logging
from copy import copy
from typing import List

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest


class TelegramHandler(logging.Handler):
    def __init__(
        self,
        *args,
        bot: Bot,
        chats_ids: List[int],
        **kwargs,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.bot = bot
        self.chats_ids = chats_ids

        try:
            self.loop = asyncio.get_event_loop()
            if not self.loop.is_running():
                raise RuntimeError("Event loop is not running.")
        except (RuntimeError, AssertionError):
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)

    def emit(self, record) -> None:
        copy_record = copy(record)
        copy_record.exc_text = None
        copy_record.exc_info = None
        msg = self.format(copy_record)
        asyncio.run_coroutine_threadsafe(self.send_log_message(msg=msg), self.loop)

    async def send_log_message(self, msg):
        for chat_id in self.chats_ids:
            try:
                await self.bot.send_message(chat_id=chat_id, text=msg)
            except TelegramBadRequest:
                await self.send_message_chunks(chat_id, msg)
            except Exception as e:
                logging.error(f"Failed to send log message to chat {chat_id}: {e}")
                self.handleError(record=f"Chat ID {chat_id}: {msg}")

    async def send_message_chunks(self, chat_id, text):
        step = 2048
        for i in range(0, len(text), step):
            await self.bot.send_message(chat_id=chat_id, text=text[i : i + step])
