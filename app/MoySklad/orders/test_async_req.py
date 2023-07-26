import asyncio
import json

import aiohttp
import time

from tqdm import tqdm


async def make_request(session, ms_id):
    async with session.get(
            f"https://online.moysklad.ru/api/remap/1.2/entity/demand/"
            f"{ms_id}/positions",
            headers={
                "Authorization": f"Bearer b707d396a2dde40ddd0d95e91badc6c7d345db4a"
            },
    ) as response:
        result = await response.json()
        try:
            return result['rows']
        except KeyError:
            return result


async def send_requests():
    with open('dataset.json', 'r', encoding='utf8') as f:
        ids = json.load(f)
        print(f'{len(ids)} requests per chunk')
    async with aiohttp.ClientSession() as session:
        tasks = []
        request_interval = 3 / 45  # Интервал между запросами в секундах

        for ms_id in tqdm(ids, desc='Async gather fetching data...', colour='GREEN'):
            task = asyncio.ensure_future(make_request(session, ms_id))
            tasks.append(task)
            await asyncio.sleep(request_interval)  # Ожидание перед следующим запросом

        responses = await asyncio.gather(*tasks)
        responses = [i for i in responses]
        print('Finished making requests')
        res = []
        for i in responses:
            res.extend(i)

        with open('res.json', 'w', encoding='utf8') as f:
            json.dump(res, f, ensure_ascii=False, indent=2)
        return len(res)


def partition(n):
    with open('dataset.json', 'r', encoding='utf8') as file:
        ids = json.load(file)

    for piece in range(0, len(ids), n):
        yield ids[piece:piece + n]


# slices = list(partition(200))
# for i in slices:
#     print(len(i))
#
# with open('res.json', 'w', encoding='utf8') as f:
#     json.dump(slices, f, ensure_ascii=False, indent=2)

start_time = time.time()
loop = asyncio.get_event_loop()
results = loop.run_until_complete(send_requests())
elapsed_time = time.time() - start_time

print(f"Время выполнения: {elapsed_time} сек.")
print(results)
