import json

from fastapi import APIRouter, status, Depends

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

    # ms_token = user_data['ms_token']
    # req = requests.get(
    #     'https://online.moysklad.ru/api/remap/1.2/entity/counterparty',
    #     headers={
    #         'Authorization': f"Bearer {ms_token}"
    #     }
    # ).json()
    #
    # with open('app/MoySklad/exmaples/CounterParties.json', 'w', encoding='utf8') as f:
    #     json.dump(req, f, ensure_ascii=False, indent=2)

    pass
