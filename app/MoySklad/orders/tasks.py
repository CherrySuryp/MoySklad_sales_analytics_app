import asyncio
import requests

from app.MoySklad.orders.dao import OrdersDAO
from app.tasks.celery_app import celery
from datetime import datetime, timedelta


@celery.task()
def get_orders(user_id: int, max_time_range: int, ms_token: str):
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
            print(request.status_code)
            request = request.json()['rows']
            content = []

            if len(request) > 0:
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
                        content.append(order_data)

                    except KeyError:
                        print(f'Failed to add order')
                        pass

                if len(content) > 0:
                    offset += 1000
                    await OrdersDAO.add_orders(content)
                    print(f"Added {len(content)} order(s)")
                else:
                    offset += 1000
                    print('No orders to add')

            else:
                break

    asyncio.get_event_loop().run_until_complete(async_get_orders())
