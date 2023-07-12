from typing import Literal

from pydantic import BaseSettings, root_validator
from sqlalchemy import NullPool


class Settings(BaseSettings):
    class Config:
        env_file = ".env"

    MODE: Literal["DEV", "TEST", "PROD"]

    API_SECRET: str

    JWT_SECRET: str
    JWT_ENCODING: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_EXPIRE: int

    @root_validator
    def get_database_url(cls, v):
        v["DATABASE_URL"] = (
            f"postgresql+asyncpg://"
            f"{v['DB_USER']}:{v['DB_PASS']}@{v['DB_HOST']}:"
            f"{v['DB_PORT']}/{v['DB_NAME']}"
        )
        return v


settings = Settings()
DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}
