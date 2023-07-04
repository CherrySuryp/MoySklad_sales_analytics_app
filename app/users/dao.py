from sqlalchemy import insert

from app.dao.dao import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


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
