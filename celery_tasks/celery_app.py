from celery import Celery
from app.config import settings

celery = Celery(
    "celery_tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.celery_tasks.celery_tasks",
        "app.MoySklad.celery_tasks",
        "app.MoySklad.items.celery_tasks",
        "app.MoySklad.sales.celery_tasks",
    ],
)
