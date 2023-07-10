from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.users.schemas import SUser
from app.MoySklad.items.tasks import get_items, celery_task

router = APIRouter(
    prefix='/ms/items',
    tags=['Items'],
)


@router.post('')
async def add_items(user_data: SUser = Depends(get_current_user)):
    celery_task.delay('bla')
