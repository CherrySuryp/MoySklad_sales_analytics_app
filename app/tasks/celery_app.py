from celery import Celery
from app.config import settings

celery = Celery(
    "tasks",
    broker=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    backend=f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
    include=[
        "app.MoySklad.tasks",

        "app.MoySklad.entities.items.tasks",
        "app.MoySklad.entities.counterparties.tasks",
        "app.MoySklad.entities.organizations.tasks",
        "app.MoySklad.entities.sales_channels.tasks",

        "app.MoySklad.orders.tasks",
        "app.MoySklad.purchases.tasks",
    ],
)
