from typing import Optional
from datetime import date

from pydantic import BaseModel, EmailStr


class SRegUser(BaseModel):
    email: EmailStr
    password: str


class SUser(BaseModel):
    id: int
    email: EmailStr
    password: str
    name: Optional[str]
    date_registered: date
    ms_token: Optional[str]
    telegram_id: Optional[int]
    verified: bool

    class Config:
        orm_mode = True
