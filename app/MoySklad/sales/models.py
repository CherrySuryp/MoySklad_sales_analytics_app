from sqlalchemy import Column, Integer, Date, ForeignKey, Computed

from app.database import Base


class Sales(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True)
    item_id = Column(ForeignKey('items.id'), nullable=False)
    sale_date = Column(Date, nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    total_cost = Column(Integer, Computed("quantity * price"))

    def __str__(self):
        return f"Sale id: {self.id}"


