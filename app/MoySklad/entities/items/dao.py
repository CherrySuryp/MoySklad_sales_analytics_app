from app.dao.base import BaseDAO
from app.MoySklad.entities.items.models import Items


class ItemsDAO(BaseDAO):
    model = Items

