import requests

from app.users.dependencies import get_current_user
from fastapi import Depends
from app.users.schemas import SUser
from fastapi import HTTPException, status


async def check_ms_token_validity(user_data: SUser = Depends(get_current_user)):
    ms_token = user_data['ms_token']
    request = requests.get(
        "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
        headers={
            'Authorization': f'Bearer {ms_token}'
        }
    )

    if request.status_code != 200:
        raise HTTPException(status_code=status.HTTP_418_IM_A_TEAPOT)
