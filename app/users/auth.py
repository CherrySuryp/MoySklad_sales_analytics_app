import datetime
from passlib.context import CryptContext
from pydantic import EmailStr
from app.users.dao import UsersDAO
from fastapi import HTTPException, status
from datetime import datetime, timedelta
from jose import jwt
from app.config import settings

passwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def encrypt_password(password: str) -> str:
    return passwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)


def create_jwt_token(data: dict) -> str:
    to_encode = data.copy()
    token_expiration = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": token_expiration})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, settings.JWT_ENCODING)
    return encoded_jwt


async def auth_user(email: EmailStr, password: str):
    user = await UsersDAO.find_one_or_none(email=email)
    if not (user and verify_password(password, user.password)):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user

