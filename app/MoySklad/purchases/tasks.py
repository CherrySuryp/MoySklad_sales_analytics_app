import asyncio
import requests

from app.MoySklad.counterparties.dao import CounterpartiesDAO
from app.MoySklad.purchases.models import Purchases, PurchaseDetails
from app.MoySklad.purchases.dao import PurchasesDAO, PurchaseDetailsDAO
from app.tasks.celery_app import celery
from datetime import datetime, timedelta


@celery.task
def get_purchases(user_id: int, max_time_range: int, ms_token: str):
    content = []

    async def async_get_purchases():
        print(f'User time range: {max_time_range}')
        date = datetime.strftime(
            datetime.utcnow() - timedelta(days=max_time_range),
            '%Y-%m-%d'
        )
        with requests.session() as session:
            offset = 0

            while True:
                data = []
                request = session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/supply"
                    f"?filter=moment>={date}",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                    params={
                        'offset': offset
                    }
                )
                request = request.json()['rows']
                print(f'Received {len(request)} orders')

                if request:
                    for i in range(len(request)):
                        try:
                            purchase_date = request[i]['moment'].split(' ')[0]
                            purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d')
                            counterparty = request[i]['agent']['meta']['href'].split('/')[-1]

                            order_data = {
                                'ms_id': request[i]['id'],
                                'user_id': user_id,
                                'name': request[i]['name'],
                                'date': purchase_date,
                                'counterparty': counterparty
                            }

                            order_exists = await PurchasesDAO.find_one_or_none(ms_id=request[i]['id'])
                            counterparty_exists = await CounterpartiesDAO.find_one_or_none(ms_id=counterparty)

                            if not order_exists and counterparty_exists:
                                data.append(order_data)
                                content.append(order_data)
                            else:
                                pass

                        except KeyError:
                            print(f'Failed to add order')
                            pass
                    if data:
                        offset += 1000
                        await PurchasesDAO.add(data)
                        print(f"Added {len(data)} order(s)")
                    else:
                        offset += 1000
                        print('No orders to add')

                else:
                    break

    asyncio.get_event_loop().run_until_complete(async_get_purchases())
    print(f'Total returned content: {len(content)}')
    return content
