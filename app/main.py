from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app.users.router import router as users_router
from app.MoySklad.router import router as ms_router
from app.MoySklad.items.router import router as ms_items_router
from app.MoySklad.orders.router import router as ms_orders_router

from redis import asyncio as aioredis
from app.config import settings

app = FastAPI()

app.include_router(users_router)
app.include_router(ms_router)
app.include_router(ms_items_router)
app.include_router(ms_orders_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(
        f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
        encoding="utf8",
        decode_responses=True
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")