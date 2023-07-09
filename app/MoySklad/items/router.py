from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
from app.users.schemas import SUser
from app.MoySklad.items.tasks import get_items

router = APIRouter(
    prefix='/ms/items',
    tags=['Items'],
)


@router.post('')
async def add_items(user_data: SUser = Depends(get_current_user)):
    user_id = user_data.id
    ms_token = user_data.ms_token
    user_limit = user_data.items_limit

    await get_items.delay(
        user_id=user_id,
        ms_token=ms_token,
        user_limit=user_limit
    )
