from app.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Date


class Purchases(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True)
    ms_id = Column(String, unique=True, nullable=False)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    counterparty = Column(ForeignKey('counterparties.ms_id'))


class PurchaseDetails(Base):
    __tablename__ = 'purchase_details'

    id = Column(Integer, primary_key=True)
    purchase_ms_id = Column(ForeignKey('purchases.ms_id'), nullable=False)
    item_ms_id = Column(ForeignKey('items.ms_id'))
    quantity = Column(Integer, nullable=False)
    sum = Column(Integer, nullable=False)

