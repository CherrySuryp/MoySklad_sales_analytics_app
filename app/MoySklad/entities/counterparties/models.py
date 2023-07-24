from app.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey


class Counterparties(Base):
    __tablename__ = 'counterparties'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    ms_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    inn = Column(String, nullable=True)