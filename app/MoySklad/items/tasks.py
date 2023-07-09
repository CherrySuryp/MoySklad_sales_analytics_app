import asyncio

import requests
from app.MoySklad.items.dao import ItemsDAO


async def get_items(ms_token: str):
    # user_id = user_data.id
    offset = 0
    while True:
        content = []
        with requests.session() as session:
            request = session.get(
                "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
                headers={
                    "Authorization": f"Bearer {ms_token}"
                },
                params={
                    'offset': 0,
                    'limit': 100,
                }
            ).json()['rows']

        request = request
        print(len(request))
        if len(request) > 0:
            for i in range(len(request)):
                try:
                    item_data = {
                        'user_id': 1,
                        'ms_id': request[i]['id'],
                        'item_code': request[i]['code'],
                        'item_external_code': request[i]['externalCode'],
                        'item_name': request[i]['name'],
                    }
                    content.append(item_data)
                except KeyError:
                    pass
            await ItemsDAO.add_items(content)
            break
        else:
            break


asyncio.run(get_items("b69cb767d2371f5242fa75e16d90bd7c05aaca31"))
