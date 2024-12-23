from pydantic import BaseModel


class Subscription(BaseModel):
    title: str
    description: str
    price: int
    payload: str
    duration_days: int
