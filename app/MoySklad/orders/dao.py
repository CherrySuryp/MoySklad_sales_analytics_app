from app.dao.base import BaseDAO
from app.MoySklad.orders.models import Orders
from app.database import async_session_maker
from sqlalchemy import insert


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def add_orders(cls, items: list):
        async with async_session_maker() as session:
            query = insert(cls.model).values(items)
            await session.execute(query)
            await session.commit()
