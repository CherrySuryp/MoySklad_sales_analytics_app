from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.tasks.tasks",
        "app.MoySklad.tasks",
        "app.MoySklad.items.tasks",
        "app.MoySklad.sales.tasks",
    ],
)
