from typing import Optional

from pydantic import BaseModel, EmailStr


class SRegUser(BaseModel):
    telegram_id: int
    name: str
    email: Optional[EmailStr] = None
    ms_token: Optional[str] = None


class SUser(BaseModel):
    id: int = 100
    telegram_id: int = 5768234
    name: str = "Mark"
    email: Optional[EmailStr] = None
    ms_token: Optional[str] = "kubqerlfbi83768"
    is_available: bool = True

    class Config:
        orm_mode = True
