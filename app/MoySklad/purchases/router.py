import json

from fastapi import APIRouter, Depends

from app.users.dependencies import get_current_user
import requests

router = APIRouter(
    tags=['Moy Sklad'],
    prefix='/MoySklad/purchases'
)

@router.post('')
async def add_purchases(user_data = Depends(get_current_user)):
    request = requests.get(
        "https://online.moysklad.ru/api/remap/1.2/entity/supply",
        headers={
            'Authorization': f'Bearer {user_data["ms_token"]}'
        }
    ).json()

    with open('app/MoySklad/exmaples/purchases_list.json', 'w', encoding='utf8') as f:
        json.dump(request, f, ensure_ascii=False, indent=2)