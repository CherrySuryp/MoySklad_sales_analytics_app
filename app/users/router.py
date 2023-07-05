from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.users.dao import UsersDAO
from app.users.schemas import SRegUser, STgUser

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/reg')
async def reg_user(user_data: SRegUser):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    await UsersDAO.add(user_data.telegram_id, user_data.name, user_data.email, user_data.ms_token)


@router.get('/{telegram_id}')
async def get_telegram_user(telegram_id: int) -> STgUser:
    existing_user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return existing_user
