from typing import Optional

from pydantic import BaseModel, EmailStr


class SRegUser(BaseModel):
    telegram_id: int
    name: str
    email: EmailStr = Optional
    ms_token: str
