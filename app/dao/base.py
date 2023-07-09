from sqlalchemy import select, insert, delete, update
from app.database import async_session_maker
from fastapi_cache.decorator import cache
from app.config import settings


class BaseDAO:
    model = None

    @classmethod
    async def add(cls, **kwargs):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def delete(cls, **kwargs):
        async with async_session_maker() as session:
            query = delete(cls.model).where(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.mappings().all()