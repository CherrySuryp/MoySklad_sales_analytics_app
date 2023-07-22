import json

from fastapi import APIRouter, status, Depends

from app.MoySklad.counterparties.tasks import get_counterparties
from app.users.dependencies import get_current_user
from app.users.schemas import SUser
import requests

router = APIRouter(
    prefix='/MoySklad/counterparties',
    tags=['Moy Sklad'],
)


@router.post(
    '',
    status_code=status.HTTP_202_ACCEPTED
)
async def add_counterparties(user_data: SUser = Depends(get_current_user)):
    user_id = user_data['id']
    ms_token = user_data['ms_token']

    get_counterparties.delay(user_id, ms_token)

    return {
        "Detail": "Task scheduled"
    }
