import requests
from fastapi_cache.decorator import cache


items = requests.get(
    "https://online.moysklad.ru/api/remap/1.2/entity/assortment",
    params={
        "limit": 1000,
        "offset": 200000
    },
    headers={
        "Authorization": "Bearer 2f3feec02a2021b5cb73ec43b4e6bbaa57a67515"
    }
)

print(items.status_code)
print(items.json()['rows'])

