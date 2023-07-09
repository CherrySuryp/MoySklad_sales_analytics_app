from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    ms_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
