import asyncio
from datetime import time

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import load_config
from core.logger import setup_logger
from handlers.base_commands import base_commands_router
from handlers.channels import channel_router
from handlers.digest import digest_router
from handlers.digest_params import digest_params_router
from handlers.subscription import notify_canceled_subscriptions, notify_expiring_subscriptions, subscription_router
from middlewear import AntiFloodMiddleware, EssenceAPIMiddleware, LoggerMiddleware
from services.daily_task_runner import run_daily_task
from services.essence_backend import EssenceBackendAPI


async def main():
    main_config = load_config()

    bot = Bot(token=main_config.bot_token)

    storage = MemoryStorage()  # TODO: change to RedisStorage
    dp = Dispatcher(storage=storage)

    # --------Loggers--------#
    logger = setup_logger(
        bot=bot,
        chats_ids=[admin.user_id for admin in main_config.admins],
        loggers_config=main_config.loggers,
    )

    # ----------Services----------#
    # redis = RedisClient(redis_config=main_config.redis)
    essence_api = EssenceBackendAPI(
        host=main_config.api_host,
        port=main_config.api_port,
        api_key=main_config.api_access_key,
    )

    # --------Middleweares--------#
    dp.message.middleware(AntiFloodMiddleware(limit=main_config.antiflood.max_message_per_sec))
    dp.message.middleware(LoggerMiddleware(logger=logger))
    dp.message.middleware(EssenceAPIMiddleware(essence_api=essence_api))

    dp.callback_query.middleware(LoggerMiddleware(logger=logger))
    dp.callback_query.middleware(EssenceAPIMiddleware(essence_api=essence_api))

    # ----------Routers-----------#
    dp.include_router(base_commands_router)
    dp.include_router(subscription_router)
    dp.include_router(channel_router)
    dp.include_router(digest_params_router)
    dp.include_router(digest_router)

    # --------Scheduled Tasks--------#
    asyncio.create_task(
        run_daily_task(
            notify_expiring_subscriptions,
            time(14, 0),
            bot=bot,
            essence_api=essence_api,
            logger=logger,
        )
    )
    asyncio.create_task(
        run_daily_task(
            notify_canceled_subscriptions,
            time(15, 0),
            bot=bot,
            essence_api=essence_api,
            logger=logger,
        )
    )

    # ----------Start bot---------#
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
