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
            email: str,
            password: str,
    ):
        async with async_session_maker() as session:
            query = insert(cls.model) \
                .values(
                email=email,
                password=password,
                date_registered=datetime.utcnow()
            )
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_all(cls):
        async with async_session_maker() as session:
            query = select(
                Users.id,
                Users.email,
                Users.password,
                Users.name,
                Users.date_registered,
                Users.ms_token,
                Users.verified
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
