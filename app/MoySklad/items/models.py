from sqlalchemy import Column, Integer, String, ForeignKey

from app.database import Base


class Items(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('users.id'), nullable=False)
    item_code = Column(String, nullable=False)
    item_external_code = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    ms_id = Column(String, unique=True, nullable=False)
