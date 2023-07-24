import asyncio
import requests

from app.MoySklad.entities.counterparties.dao import CounterpartiesDAO
from app.MoySklad.entities.items.dao import ItemsDAO
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


@celery.task
def get_purchase_details(content: list, ms_token: str):
    if not content:
        return

    data = []

    async def async_get_purchase_details():
        count = 0
        with requests.session() as session:
            for i in range(len(content)):
                purchase_ms_id = content[i]['ms_id']
                request = session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/supply/"
                    f"{purchase_ms_id}/positions",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                )
                request = request.json()['rows']

                count += 1
                print(f"Request No: {count}")

                for a in range(len(request)):
                    item_ms_id = request[a]['assortment']['meta']['href']
                    item_ms_id = item_ms_id.split('/')[-1]
                    # try:
                    purchase_details = {
                        "purchase_ms_id": purchase_ms_id,
                        'item_ms_id': item_ms_id,
                        'quantity': request[a]['quantity'],
                        'sum': request[a]['price'],
                    }

                    order_details_exists = await PurchaseDetailsDAO.find_one_or_none(
                        purchase_ms_id=purchase_ms_id,
                        item_ms_id=purchase_details['item_ms_id']
                    )

                    item_exists = await ItemsDAO.find_one_or_none(ms_id=item_ms_id)

                    if order_details_exists or not item_exists:
                        pass
                    else:
                        data.append(purchase_details)

            # except IndentationError:
            #     print(f'Failed to add order_details')
            #     pass

        if data:
            await PurchaseDetailsDAO.add(data)
            print(f"Added {len(data)} order details")
        else:
            print('No order details to add')

    asyncio.get_event_loop().run_until_complete(async_get_purchase_details())
