from app.dao.base import BaseDAO
from app.MoySklad.items.models import Items
from sqlalchemy import insert

from app.database import async_session_maker


class ItemsDAO(BaseDAO):
    model = Items

    @classmethod
    async def add_items(cls, items: list):
        async with async_session_maker() as session:
            query = insert(cls.model).values(items)
            await session.execute(query)
            await session.commit()
