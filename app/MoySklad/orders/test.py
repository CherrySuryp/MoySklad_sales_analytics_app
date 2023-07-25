import asyncio

import aiohttp


# async def test():
#     async with aiohttp.ClientSession() as session:
#         request = await session.get(
#             f"https://online.moysklad.ru/api/remap/1.2/entity/demand",
#             headers={
#                 "Authorization": f"Bearer b707d396a2dde40ddd0d95e91badc6c7d345db4a"
#             },
#             params={
#                 'limit': 1,
#                 'offset': 2
#             }
#         )
#         request = await request.json()
#         request = request['rows']
#
#         print(len(request))
#
#
# asyncio.run(test())
