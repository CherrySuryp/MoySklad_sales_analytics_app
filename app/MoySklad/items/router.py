from fastapi import APIRouter, Depends, status

from app.MoySklad.items.tasks import get_items
from app.users.dependencies import get_current_user
from app.users.schemas import SUser

router = APIRouter(
    prefix='/MoySklad/items',
    tags=['Moy Sklad'],
)


@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def add_items(user_data: SUser = Depends(get_current_user)):
    if not isinstance(user_data, dict):
        user_data = user_data.__dict__

    user_id = user_data['id']
    ms_token = user_data['ms_token']
    user_limit = user_data['items_limit']
    get_items.delay(user_id, ms_token, user_limit)

    return {
        "Detail": "Task Scheduled"
    }
