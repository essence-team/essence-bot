from enum import Enum

from pydantic import BaseModel


class DigestFreq(Enum):
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class User(BaseModel):
    user_id: str
    username: str
    digest_freq: DigestFreq
    digest_time: int
    remaining_days: int | None
