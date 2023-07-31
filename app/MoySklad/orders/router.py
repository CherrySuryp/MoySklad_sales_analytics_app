from fastapi import APIRouter, status, Depends

from app.MoySklad.dependecies import check_ms_token_validity
from app.users.schemas import SUser
from app.users.dependencies import get_current_user
from app.MoySklad.orders.tasks import get_orders, get_order_details
from celery import chain
router = APIRouter(
    prefix='/MoySklad/orders',
    tags=['Moy Sklad'],
    dependencies=[Depends(check_ms_token_validity)]
)


@router.post(
    '',
    status_code=status.HTTP_202_ACCEPTED,
)
async def add_orders_and_order_details(user_data: SUser = Depends(get_current_user)):

    user_id = user_data['id']
    ms_token = user_data['ms_token']
    max_time_range = user_data['max_time_range']
    chain(
        get_orders.s(user_id, max_time_range, ms_token),
        get_order_details.s(ms_token)
    ).delay()

    return {
        "Detail": "Task scheduled"
    }
