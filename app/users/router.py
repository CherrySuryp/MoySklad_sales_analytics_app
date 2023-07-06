import asyncio
from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from app.config import settings
from app.users.dao import UsersDAO
from app.users.dependencies import check_api_token
from app.users.schemas import SRegUser, SUser
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post(
    '/reg',
    dependencies=[Depends(check_api_token)],
)
async def reg_user(user_data: SRegUser):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    await UsersDAO.add(user_data.telegram_id, user_data.name, user_data.email, user_data.ms_token)


@router.get("", dependencies=[Depends(check_api_token)])
async def get_users() -> list[SUser]:
    users = await UsersDAO.find_all()
    return users


@router.get('/{telegram_id}', dependencies=[Depends(check_api_token)])
@cache(expire=settings.REDIS_EXPIRE, namespace='User')
async def get_telegram_user(telegram_id: int) -> SUser:
    await asyncio.sleep(5)
    existing_user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    return existing_user


@router.put(
    '/{telegram_id}/update_token',
    dependencies=[Depends(check_api_token)],
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_ms_token(
        telegram_id: int,
        token: str
):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    await UsersDAO.update_token(telegram_id, token)
