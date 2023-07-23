import json

from fastapi import APIRouter, Depends

from app.MoySklad.purchases.tasks import get_purchases
from app.users.dependencies import get_current_user
import requests

router = APIRouter(
    tags=['Moy Sklad'],
    prefix='/MoySklad/purchases'
)


@router.post('')
async def add_purchases(user_data=Depends(get_current_user)):
    user_id = user_data['id']
    ms_token = user_data['ms_token']
    max_time_range = user_data['max_time_range']

    get_purchases.delay(user_id, max_time_range, ms_token)

    return {
        'Detail': 'Task scheduled'
    }

