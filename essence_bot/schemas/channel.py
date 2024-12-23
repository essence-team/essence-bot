from pydantic import BaseModel


class ChannelAddResponse(BaseModel):
    channel_link: str
    exists: bool


class ChannelResponse(BaseModel):
    channel_link: str
