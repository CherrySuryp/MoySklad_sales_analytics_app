from sqlalchemy import select, insert, delete
from app.database import async_session_maker
from sqlalchemy.exc import IntegrityError


class BaseDAO:
    model = None

    @classmethod
    async def add_many(cls, *args):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(*args)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                print(e)

    @classmethod
    async def add_one(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                query = insert(cls.model).values(**kwargs)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                print(e)

    @classmethod
    async def delete(cls, **kwargs):
        async with async_session_maker() as session:
            try:
                query = delete(cls.model).where(**kwargs)
                await session.execute(query)
                await session.commit()
            except IntegrityError as e:
                print(e)

    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.mappings().all()
            except IntegrityError as e:
                print(e)

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            try:
                query = select(cls.model).filter_by(**filter_by)
                result = await session.execute(query)
                return result.scalar_one_or_none()
            except IntegrityError as e:
                print(e)
