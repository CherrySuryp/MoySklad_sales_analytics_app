from sqlalchemy import insert

from app.dao.base import BaseDAO
from app.MoySklad.counterparties.models import Counterparties
from app.database import async_session_maker


class CounterpartiesDAO(BaseDAO):
    model = Counterparties

    @classmethod
    async def add_counterparties(cls, counterparties: list):
        async with async_session_maker() as session:
            query = insert(cls.model).values(counterparties)
            await session.execute(query)
            await session.commit()
