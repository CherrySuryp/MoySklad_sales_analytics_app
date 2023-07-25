from app.dao.base import BaseDAO
from app.MoySklad.entities.counterparties.models import Counterparties


class CounterpartiesDAO(BaseDAO):
    model = Counterparties
