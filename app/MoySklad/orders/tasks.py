import asyncio
import json

import aiohttp
from tqdm import tqdm

from app.MoySklad.entities.counterparties.dao import CounterpartiesDAO
from app.MoySklad.orders.dao import OrdersDAO, OrderDetailsDAO
from app.MoySklad.entities.items.dao import ItemsDAO
from app.tasks.celery_app import celery
from datetime import datetime, timedelta


@celery.task
def get_orders(user_id: int, max_time_range: int, ms_token: str):
    content = []

    async def async_get_orders():
        print(f'User time range: {max_time_range}')
        date = datetime.strftime(
            datetime.utcnow() - timedelta(days=max_time_range),
            '%Y-%m-%d'
        )
        async with aiohttp.ClientSession() as session:
            offset = 0

            while True:
                data = []
                request = await session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/demand"
                    f"?filter=moment>={date}",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                    params={
                        'offset': offset
                    }
                )
                request = await request.json()
                request = request['rows']
                print(f'Received {len(request)} orders')

                if request:
                    for i in range(len(request)):
                        try:
                            order_date = request[i]['moment'].split(' ')[0]
                            order_date = datetime.strptime(order_date, '%Y-%m-%d')
                            counterparty = request[i]['agent']['meta']['href'].split('/')[-1]

                            order_data = {
                                'ms_id': request[i]['id'],
                                'user_id': user_id,
                                'order_name': request[i]['name'],
                                'order_date': order_date,
                                'counterparty': counterparty
                            }

                            order_exists = await OrdersDAO.find_one_or_none(ms_id=request[i]['id'])
                            counterparty_exists = await CounterpartiesDAO.find_one_or_none(ms_id=counterparty)

                            if not order_exists and counterparty_exists:
                                data.append(order_data)
                                content.append(order_data['ms_id'])
                            else:
                                pass

                        except KeyError:
                            print(f'Failed to add order')
                            pass
                    if data:
                        offset += 1000
                        await OrdersDAO.add_many(data)
                        print(f"Added {len(data)} order(s)")
                    else:
                        offset += 1000
                        print('No orders to add')

                else:
                    break

    asyncio.get_event_loop().run_until_complete(async_get_orders())

    print(f'Total returned content: {len(content)}')
    return content


@celery.task
def get_order_details(content: list, ms_token: str):
    if not content:
        return

    data = []

    async def async_get_order_details():
        count = 0
        async with aiohttp.ClientSession() as session:
            for order_ms_id in content:
                request = await session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/demand/"
                    f"{order_ms_id}/positions",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                )
                request = await request.json()
                request = request['rows']

                count += 1

                for a in range(len(request)):
                    product_ms_id = request[a]['assortment']['meta']['href']
                    product_ms_id = product_ms_id.split('/')[-1]
                    order_details = {
                        "order_ms_id": order_ms_id,
                        'product_ms_id': product_ms_id,
                        'quantity': request[a]['quantity'],
                        'sum': request[a]['price'],
                    }
                    order_details_exists = await OrderDetailsDAO.find_one_or_none(
                        order_ms_id=order_ms_id,
                        product_ms_id=order_details['product_ms_id']
                    )

                    item_exists = await ItemsDAO.find_one_or_none(ms_id=product_ms_id)
                    if order_details_exists or not item_exists:
                        pass
                    else:
                        data.append(order_details)
        if data:
            await OrderDetailsDAO.add_many(data)
            print(f"Added {len(data)} order details")
        else:
            print('No order details to add')

    asyncio.get_event_loop().run_until_complete(async_get_order_details())
