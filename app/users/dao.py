from fastapi import HTTPException, status
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError

from app.dao.dao import BaseDAO
from app.database import async_session_maker
from app.users.models import Users

from datetime import datetime


class UsersDAO(BaseDAO):
    model = Users

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
                    date_registered=datetime.utcnow()
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
            query = select(
                Users.id,
                Users.telegram_id,
                Users.name,
                Users.email,
                Users.ms_token,
                Users.is_available,
                Users.date_registered,
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def update_token(cls, user_id, new_token):
        async with async_session_maker() as session:
            query = (
                update(cls.model).
                where(cls.model.id == user_id).
                values(ms_token=new_token)
            )
            await session.execute(query)
            await session.commit()
            
