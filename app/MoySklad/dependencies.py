import requests
from fastapi import Depends, HTTPException, status

from app.users.dependencies import get_current_user


async def check_ms_token(user_data: dict = Depends(get_current_user)):
    ms_token = user_data['ms_token']
    req = requests.get(
        'https://online.moysklad.ru/api/remap/1.2/entity/assortment',
        headers={
            f"Authorization: Bearer {ms_token}",
        },
        params={
            'limit': 1,
            'offset': 10000000000000000
        }
    )
    print(req.status_code)

    if req.status_code != 200:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
