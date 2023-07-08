from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr


class SRegUser(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    telegram_id: int
    name: str
    email: Optional[EmailStr]
    ms_token: Optional[str]
    is_available: bool
    date_registered: date

    class Config:
        orm_mode = True
