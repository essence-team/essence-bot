from pydantic import BaseModel


class Antiflood(BaseModel):
    max_message_per_sec: int
