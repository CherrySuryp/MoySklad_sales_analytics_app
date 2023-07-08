from fastapi import APIRouter, status, Depends, Response
from fastapi.exceptions import HTTPException

from app.users.auth import encrypt_password, auth_user, create_jwt_token
from app.users.dao import UsersDAO
from app.dependencies import check_api_token
from app.users.schemas import SRegUser, SUser

from datetime import datetime, timedelta


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
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='User already exists'
        )
    hashed_passwd = encrypt_password(user_data.password)
    await UsersDAO.add(email=user_data.email, password=hashed_passwd)


@router.post(
    '/login',
    status_code=status.HTTP_202_ACCEPTED
)
async def login_user(user_data: SRegUser, response: Response):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_jwt_token({"user_id": str(user.id)})
    response.set_cookie(
        "MS_Analytics",
        access_token,
        httponly=True,
    )
    return {"JWT Token": access_token}


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
