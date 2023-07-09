import asyncio

import requests
from app.MoySklad.items.dao import ItemsDAO
from app.tasks.celery_app import celery
from app.users.schemas import SUser


@celery.task()
async def get_items(user_id: int, ms_token: str, user_limit: int):

    offset = 0
    while offset <= user_limit:
        content = []

        # Getting items from MoySklad API
        with requests.session() as session:
            request = session.get(
                "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
                headers={
                    "Authorization": f"Bearer {ms_token}"
                },
                params={
                    'offset': offset,
                    'limit': user_limit,
                }
            ).json()['rows']

        request = request

        if len(request) > 0:
            for i in range(len(request)):
                try:
                    item_data = {
                        'user_id': user_id,
                        'ms_id': request[i]['id'],
                        'item_code': request[i]['code'],
                        'item_external_code': request[i]['externalCode'],
                        'item_name': request[i]['name'],
                    }

                    item_exists = await ItemsDAO.find_one_or_none(
                        ms_id=item_data['ms_id'],
                        user_id=1
                    )

                    if item_exists is not None:
                        pass
                    else:
                        content.append(item_data)
                except KeyError:
                    pass

            if len(content) > 0:
                offset += 1000
                await ItemsDAO.add_items(content)
                print(f"Added {len(content)} items")
            else:
                print('No items to add')
        else:
            break
