from dotenv import load_dotenv
import os

load_dotenv()


class Settings:
    MODE = os.environ.get('MODE')

    API_SECRET = os.environ.get('API_SECRET')

    JWT_SECRET = os.environ.get('JWT_SECRET')
    JWT_ENCODING = os.environ.get('JWT_ENCODING')

    DB_HOST = os.environ.get('DB_HOST')
    DB_PORT = os.environ.get('DB_PORT')
    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    DB_NAME = os.environ.get('DB_NAME')

    REDIS_HOST = os.environ.get('REDIS_HOST')
    REDIS_PORT = os.environ.get('REDIS_PORT')
    REDIS_EXPIRE = os.environ.get('REDIS_EXPIRE')

    DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


settings = Settings()
DATABASE_URL = settings.DATABASE_URL
DATABASE_PARAMS = {}
