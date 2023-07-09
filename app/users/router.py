from fastapi import APIRouter, status, Depends, Response
from fastapi.exceptions import HTTPException

from app.users.auth import encrypt_password, auth_user, create_jwt_token
from app.users.dao import UsersDAO
from app.dependencies import check_api_token  # noqa
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SRegUser, SUser

router = APIRouter(
    prefix='/users',
    tags=['Users'],
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
    return {"Detail": "User Registered"}


@router.post(
    '/login',
    status_code=status.HTTP_202_ACCEPTED
)
async def login_user(user_data: SRegUser, response: Response):
    user = await auth_user(user_data.email, user_data.password)
    access_token = create_jwt_token({"sub": str(user.id)})
    response.set_cookie(
        "MS_Analytics",
        access_token,
        httponly=True,
    )
    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie('MS_Analytics')


@router.get("/me")
async def get_current_user(user: Users = Depends(get_current_user)):
    return user


@router.put(
    '/update_ms_token',
    status_code=status.HTTP_202_ACCEPTED
)
async def update_ms_token(
        token: str,
        user: Users = Depends(get_current_user),
):
    user_id = user.id
    existing_user = await UsersDAO.find_one_or_none(id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User does not exist'
        )
    await UsersDAO.update_token(user_id, token)


@router.get("", dependencies=[Depends(check_api_token)])
async def get_users() -> list[SUser]:
    users = await UsersDAO.find_all()
    return users
