from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException

from app.users.dao import UsersDAO

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/reg')
async def reg_user(
        telegram_id: int,
        name: str,
        email: str,
        ms_token: str,
):
    existing_user = await UsersDAO.find_one_or_none(telegram_id=telegram_id)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
    await UsersDAO.add(telegram_id, name, email, ms_token)
