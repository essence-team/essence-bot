from pydantic import BaseModel


class Admin(BaseModel):
    """Данные, которые должны быть указаны для админа"""

    user_id: int
    username: str
