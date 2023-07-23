from app.dao.base import BaseDAO
from app.MoySklad.purchases.models import Purchases
from app.MoySklad.purchases.models import PurchaseDetails


class PurchasesDAO(BaseDAO):
    model = Purchases


class PurchaseDetailsDAO(BaseDAO):
    model = PurchaseDetails

