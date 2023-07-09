from fastapi import APIRouter, Depends

from app.MoySklad.items.tasks import get_items
from app.users.dependencies import get_current_user
from app.users.schemas import SUser
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/MoySklad',
    tags=['Moy Sklad']
)
