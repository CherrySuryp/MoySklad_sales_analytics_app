from fastapi import APIRouter, Depends
from celery import chain

from app.MoySklad.dependecies import check_ms_token_validity
from app.MoySklad.purchases.tasks import get_purchases, get_purchase_details
from app.users.dependencies import get_current_user

router = APIRouter(
    tags=['Moy Sklad'],
    prefix='/MoySklad/purchases',
    dependencies=[Depends(check_ms_token_validity)]
)


@router.post('')
async def add_purchases(user_data=Depends(get_current_user)):
    user_id = user_data['id']
    ms_token = user_data['ms_token']
    max_time_range = user_data['max_time_range']

    chain(
        get_purchases.s(user_id, max_time_range, ms_token),
        get_purchase_details.s(ms_token)
    ).apply_async()

    return {
        'Detail': 'Task scheduled'
    }
