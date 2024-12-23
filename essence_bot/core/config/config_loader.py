from typing import List

import yaml
from core.config.models.admin import Admin
from core.config.models.antiflood import Antiflood
from core.config.models.loggers import LoggersConfig
from core.config.models.subscription import Subscription
from dotenv import load_dotenv
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    env: str

    bot_token: str
    provider_token: str

    admins: List[Admin]

    api_host: str
    api_port: int
    api_access_key: str

    subscriptions: List[Subscription]

    antiflood: Antiflood
    loggers: LoggersConfig


def load_yaml_config(file_path: str):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)


def load_config() -> Config:
    load_dotenv(dotenv_path=".env", verbose=True)

    yaml_config = load_yaml_config("essence_bot/core/config/config.yaml")
    loggers = LoggersConfig()
    settings = Config(**yaml_config, loggers=loggers)

    return settings
