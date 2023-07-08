from jose import jwt, JWTError
from app.config import settings
from app.users.dao import UsersDAO
from fastapi import Request, HTTPException, status, Depends


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

    user_id: str = payload.get('sub')
    if not user_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

