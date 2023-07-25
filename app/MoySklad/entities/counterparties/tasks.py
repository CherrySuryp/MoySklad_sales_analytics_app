import asyncio
import requests

from app.MoySklad.entities.counterparties.dao import CounterpartiesDAO
from app.tasks.celery_app import celery


@celery.task
def get_counterparties(user_id: int, ms_token: str):
    async def async_get_counterparties():
        with requests.session() as session:
            offset = 0

            while True:
                data = []
                request = session.get(
                    "https://online.moysklad.ru/api/remap/1.2/entity/counterparty",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                    params={
                        'offset': offset
                    }
                )
                request = request.json()['rows']

                if request:
                    for i in range(len(request)):
                        try:
                            inn = request[i]['inn']
                        except KeyError:
                            inn = None

                        try:

                            order_data = {
                                'user_id': user_id,
                                'ms_id': request[i]['id'],
                                'name': request[i]['name'],
                                'inn': inn,
                            }

                            counterparty_exists = await CounterpartiesDAO.find_one_or_none(ms_id=request[i]['id'])

                            if not counterparty_exists:
                                data.append(order_data)
                            else:
                                pass

                        except KeyError:
                            print(f'Failed to add order')
                            pass
                    if data:
                        offset += 1000
                        await CounterpartiesDAO.add_many(data)
                        print(f"Added {len(data)} counterparties")
                    else:
                        offset += 1000
                        print('No counterparties to add')

                else:
                    break

    asyncio.get_event_loop().run_until_complete(async_get_counterparties())
