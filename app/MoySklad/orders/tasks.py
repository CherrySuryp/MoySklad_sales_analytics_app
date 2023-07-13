import asyncio
import requests

from app.MoySklad.orders.dao import OrdersDAO, OrderDetailsDAO
from app.MoySklad.items.dao import ItemsDAO
from app.tasks.celery_app import celery
from datetime import datetime, timedelta


@celery.task
def get_orders(user_id: int, max_time_range: int, ms_token: str):
    content = []

    async def async_get_orders():
        print(f'User time range: {max_time_range}')

        offset = 0
        date = datetime.strftime(
            datetime.utcnow() - timedelta(days=max_time_range),
            '%Y-%m-%d'
        )

        while True:
            with requests.session() as session:
                request = session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/demand"
                    f"?filter=moment>={date}",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                    params={
                        'offset': offset,
                        'limit': 1000
                    }
                )
            request = request.json()['rows']

            if request:
                for i in range(len(request)):
                    try:
                        order_date = request[i]['moment'].split(' ')[0]
                        order_date = datetime.strptime(order_date, '%Y-%m-%d')
                        order_data = {
                            'ms_id': request[i]['id'],
                            'user_id': user_id,
                            'order_name': request[i]['name'],
                            'order_date': order_date,
                        }

                        order_exists = await OrdersDAO.find_one_or_none(ms_id=request[i]['id'])
                        if order_exists:
                            pass
                        else:
                            content.append(order_data)

                    except KeyError:
                        print(f'Failed to add order')
                        pass

                if content:
                    offset += 1000
                    await OrdersDAO.add_orders(content)
                    print(f"Added {len(content)} order(s)")
                else:
                    offset += 1000
                    print('No orders to add')

            else:
                break

    asyncio.get_event_loop().run_until_complete(async_get_orders())
    return content


@celery.task
def get_order_details(content: list, ms_token: str):
    if not content:
        return

    data = []

    async def async_get_order_details():
        for i in range(len(content)):
            order_ms_id = content[i]['ms_id']

            with requests.session() as session:
                request = session.get(
                    f"https://online.moysklad.ru/api/remap/1.2/entity/demand/"
                    f"{order_ms_id}/positions",
                    headers={
                        "Authorization": f"Bearer {ms_token}"
                    },
                )
            print(request.status_code)
            request = request.json()['rows']

            for a in range(len(request)):
                product_ms_id = request[a]['assortment']['meta']['href']
                product_ms_id = product_ms_id.split('/')[-1]
                # try:
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

            # except IndentationError:
            #     print(f'Failed to add order_details')
            #     pass

        if data:
            await OrderDetailsDAO.add_order_details(data)
            print(f"Added {len(data)} order details")
        else:
            print('No order details to add')

    asyncio.get_event_loop().run_until_complete(async_get_order_details())
