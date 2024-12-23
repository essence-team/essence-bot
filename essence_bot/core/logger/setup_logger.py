import logging
from typing import List

from aiogram import Bot
from core.config.models.loggers import LoggersConfig
from core.logger.tg_handler import TelegramHandler

# from logstash_async.formatter import LogstashFormatter
# from logstash_async.handler import SynchronousLogstashHandler


# Настройка основного логгера
def setup_logger(
    bot: Bot,
    chats_ids: List[int],
    loggers_config: LoggersConfig,
) -> logging.Logger:
    logger = logging.getLogger("telegram_bot")
    logger.setLevel(logging.DEBUG)

    # TelegramHandler
    telegram_handler = TelegramHandler(bot=bot, chats_ids=chats_ids)
    telegram_handler.setLevel(logging.ERROR)
    telegram_formatter = logging.Formatter("%(asctime)s\n%(levelname)s\n%(msg)s\n%(filename)s:%(funcName)s:%(lineno)s")
    telegram_handler.setFormatter(telegram_formatter)
    logger.addHandler(telegram_handler)

    # ConsoleHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    # console_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # console_handler.setFormatter(console_formatter)
    # logger.addHandler(console_handler)

    # Настройка логгера aiogram
    aiogram_logger = logging.getLogger("aiogram")
    aiogram_logger.setLevel(logging.DEBUG)
    aiogram_logger.addHandler(console_handler)

    # LogstashHandler
    # logstash_handler = SynchronousLogstashHandler(
    #     host=loggers_config.logstash_host,
    #     port=loggers_config.logstash_port,
    #     database_path=None,
    # )
    # logstash_handler.setLevel(logging.INFO)
    # logstash_formatter = LogstashFormatter(
    #     message_type="python-log",
    #     extra_prefix="extra",
    #     extra=dict(environment=loggers_config.logs_env, application="telegram_bot"),
    # )
    # logstash_handler.setFormatter(logstash_formatter)
    # logger.addHandler(logstash_handler)

    # # GrayLog
    # graylog_handler = GelfUdpHandler(host=loggers_config.graylogger_host, port=loggers_config.graylogger_port)
    # graylog_handler.setLevel(logging.DEBUG)
    # graylog_formatter = logging.Formatter(
    #     "%(asctime)s - %(levelname)s - %(msg)s - %(filename)s:%(funcName)s:%(lineno)s",
    # )
    # graylog_handler.setFormatter(graylog_formatter)
    # logger.addHandler(graylog_handler)

    return logger
