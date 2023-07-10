import asyncio

from fastapi_cache import JsonCoder
from jose import jwt, JWTError
from app.config import settings
from app.users.dao import UsersDAO
from fastapi import Request, HTTPException, status, Depends
from fastapi_cache.decorator import cache


def get_token(request: Request):
    token = request.cookies.get("MS_Analytics")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, settings.JWT_ENCODING)
    except JWTError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)

    user_id: int = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    @cache(expire=5, coder=JsonCoder)
    async def get_user(uid: int):
        await asyncio.sleep(2)
        user = await UsersDAO.find_one_or_none(id=int(uid))
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return user

    return await get_user(user_id)

