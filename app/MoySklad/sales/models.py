from sqlalchemy import Column, Integer, Date, String, ForeignKey

from app.database import Base
from app.users.models import Users


class Orders(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    ms_id = Column(String, unique=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    order_date = Column(Date, nullable=False)


class OrderDetails(Base):
    __tablename__ = 'order_details'

    id = Column(Integer, primary_key=True)
    order_ms_id = Column(ForeignKey('orders.ms_id'), nullable=False)
    product_ms_id = Column(ForeignKey('items.ms_id'), nullable=False),
    quantity = Column(Integer, nullable=False)
    sum = Column(Integer, nullable=False)


