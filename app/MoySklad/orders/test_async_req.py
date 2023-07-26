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


def slice_list_to_chunks(to_slice: list, chunk_size: int):
    for piece in range(0, len(to_slice), chunk_size):
        yield to_slice[piece:piece + chunk_size]


async def send_requests():
    start_time = time.time()

    result = []
    with open('dataset.json', 'r', encoding='utf8') as f:
        ids = json.load(f)

    chunk_size = 200
    chunks = list(slice_list_to_chunks(ids, chunk_size))

    print(f'{len(ids)} requests to make')
    print(f"{chunk_size} requests per chunk")

    for chunk in tqdm(chunks, desc='Proceeding chunks...', colour='GREEN'):

        async with aiohttp.ClientSession() as session:

            tasks = []
            request_interval = 3 / 45  # Интервал между запросами в секундах

            for ms_id in chunk:
                task = asyncio.ensure_future(make_request(session, ms_id))
                tasks.append(task)
                await asyncio.sleep(request_interval)  # Ожидание перед следующим запросом

            result.extend(await asyncio.gather(*tasks))

            await session.close()

    with open('res.json', 'w', encoding='utf8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    elapsed_time = time.time() - start_time

    print(f"Execution time: {elapsed_time} secs.")
    print(f"Requests made: {len(ids)}")
    print(f"Requests per async task: {chunk_size}")
    print(f'Actual RPS: {len(ids) / elapsed_time}')


loop = asyncio.get_event_loop()
loop.run_until_complete(send_requests())
