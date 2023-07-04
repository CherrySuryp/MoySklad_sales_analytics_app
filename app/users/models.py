from sqlalchemy import Column, Integer, String, Boolean

from app.database import Base


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)
    ms_token = Column(String, unique=True)
    is_available = Column(Boolean, default=True, nullable=False)

    def __str__(self):
        return f"User: {self.email}"
