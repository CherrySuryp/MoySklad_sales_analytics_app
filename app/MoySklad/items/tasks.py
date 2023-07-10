import asyncio

import requests
from app.MoySklad.items.dao import ItemsDAO
from app.tasks.celery_app import celery


@celery.task()
def get_items(user_id: int, ms_token: str, user_limit: int):
    async def async_get_items():

        offset = 0
        while offset < user_limit:
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
            content = []

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
                            user_id=user_id
                        )
                        if not item_exists:
                            content.append(item_data)
                        else:
                            pass
                    except KeyError:
                        pass

                if len(content) > 0:
                    offset += 1000
                    await ItemsDAO.add_items(content)
                    print(f"Added {len(content)} items")
                else:
                    offset += 1000
                    print('No items to add')
            else:
                break

    asyncio.get_event_loop().run_until_complete(async_get_items())
