from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException

from app.users.dao import UsersDAO
from app.dependencies import check_api_token
from app.users.schemas import SRegUser, SUser

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    dependencies=[Depends(check_api_token)]
)


@router.post(
    '/reg',
    status_code=status.HTTP_201_CREATED
)
async def reg_user(user_data: SRegUser):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=user_data.telegram_id)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    await UsersDAO.add(user_data.telegram_id, user_data.name, user_data.email, user_data.ms_token)


@router.get('/{user_id}')
async def get_user_by_id(user_id: int) -> SUser:
    existing_user = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    return existing_user


@router.put(
    '/{user_id}/update_token',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_ms_token(
        user_id: int,
        token: str
):
    existing_user = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    await UsersDAO.update_token(user_id, token)


@router.get("")
async def get_users():
    users = await UsersDAO.find_all()
    return users
