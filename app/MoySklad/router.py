from fastapi import APIRouter, Depends
from app.users.dependencies import get_current_user
from app.users.schemas import SUser
from fastapi_cache.decorator import cache

router = APIRouter(
    prefix='/MoySklad',
    tags=['Moy Sklad']
)


@router.post('/update_items')
@cache(expire=30)
def get_items_from_ms(user_data: SUser = Depends(get_current_user)):
    return user_data.id
