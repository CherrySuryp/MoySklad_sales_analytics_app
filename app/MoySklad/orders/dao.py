from app.dao.base import BaseDAO
from app.MoySklad.orders.models import Orders, OrderDetails


class OrdersDAO(BaseDAO):
    model = Orders


class OrderDetailsDAO(BaseDAO):
    model = OrderDetails
