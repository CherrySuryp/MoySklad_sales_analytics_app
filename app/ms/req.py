import requests


async def get_items(user_id, token):
    items = requests.get(
        "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
        params={
            "limit": 1000,
            "offset": 0
        },
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    

