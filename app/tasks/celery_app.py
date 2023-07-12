from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.MoySklad.tasks",
        "app.MoySklad.items.tasks",
        "app.MoySklad.orders.tasks",
    ],
)
