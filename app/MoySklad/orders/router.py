from fastapi import APIRouter, status, Depends
from app.users.schemas import SUser
from app.users.dependencies import get_current_user
from app.MoySklad.orders.tasks import get_orders

router = APIRouter(
    prefix='/MoySklad/orders',
    tags=['Moy Sklad']
)


@router.post('', status_code=status.HTTP_202_ACCEPTED)
async def add_orders(user_data: SUser = Depends(get_current_user)):

    user_id = user_data['id']
    ms_token = user_data['ms_token']
    max_time_range = user_data['max_time_range']

    get_orders.delay(user_id, max_time_range, ms_token)
