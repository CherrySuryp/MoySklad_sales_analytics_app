from sqlalchemy import Column, Integer, String, Boolean, Date

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String)
    date_registered = Column(Date)
    ms_token = Column(String)
    telegram_id = Column(Integer)
    verified = Column(Boolean, default=False, nullable=False)
    items_limit = Column(Integer, default=1000, nullable=False)
    max_time_range = Column(Integer, default=12)
