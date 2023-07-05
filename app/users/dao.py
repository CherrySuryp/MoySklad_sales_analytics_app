from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from app.dao.dao import BaseDAO
from app.database import async_session_maker
from app.users.models import UsersTelegram


class UsersDAO(BaseDAO):
    model = UsersTelegram

    @classmethod
    async def add(
            cls,
            telegram_id: int,
            name: str,
            email: str,
            ms_token: str,
            is_available: bool = True,
    ):
        try:
            async with async_session_maker() as session:
                query = insert(cls.model)\
                    .values(
                    telegram_id=telegram_id,
                    name=name,
                    email=email,
                    ms_token=ms_token,
                    is_available=is_available,
                )
                await session.execute(query)
                await session.commit()

        except (IntegrityError, Exception):

            if IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Wrong MS token format or it's already in use"
                )
            elif Exception:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="An error occurred"
                )

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(UsersTelegram)
            result = await session.execute(query)
            return result.scalars()

    @classmethod
    async def update_token(cls, telegram_id, new_token):
        async with async_session_maker() as session:
            query = (
                update(cls.model).
                where(cls.model.telegram_id == telegram_id).
                values(ms_token=new_token)
            )
            await session.execute(query)
            await session.commit()
            
