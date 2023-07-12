"""Получение остатков товаров по сладам
"""
import logging
from dataclasses import dataclass
from typing import Self
from .products import OzonProduct
from .api import OzonAPI

logger = logging.getLogger("Strite")


@dataclass(frozen=True)
class OzonWarehouse:
    id: str
    name: str

    @classmethod
    def get_warehouses(cls, api: OzonAPI) -> list[Self]:
        raw_data = api.request(url="v1/supplier/available_warehouses",
                               method="GET")

        if not raw_data.get('result', False):
            logger.error(msg := "Не смогли получить транзакции магазина Ozon")
            raise Exception(msg)

        for warehouse in raw_data['result']:
            yield cls(
                id=warehouse["warehouse"]["id"],
                name=warehouse["warehouse"]["name"],
            )

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "name": self.name
        }


@dataclass(frozen=True)
class OzonStockOnWarehouse:
    sku: int
    vendor_code: str
    free_to_sell_amount: int  # Количество товара, доступное к продаже
    promised_amount: int  #
    reserved_amount: int
    warehouse: OzonWarehouse

    def get_product(self) -> OzonProduct:
        raise NotImplemented

    @classmethod
    def get_stocks(cls, api: OzonAPI) -> list[Self]:
        warehouses = list(OzonWarehouse.get_warehouses(api))

        body = {
            "limit": 1000,
            "offset": 0,
            "warehouse_type": "ALL"
        }

        while True:
            raw_data = api.request(url="v2/analytics/stock_on_warehouses",
                                   method="POST",
                                   json=body)

            if not raw_data.get('result', False):
                logger.error(msg := "Не смогли получить транзакции магазина Ozon")
                raise Exception(msg)

            for row in raw_data['result']['rows']:
                warehouse = [w for w in warehouses if w.name == row["warehouse_name"]][0]

                yield cls(
                    sku=row["sku"],
                    vendor_code=row["item_code"],
                    free_to_sell_amount=row["free_to_sell_amount"],
                    promised_amount=row["promised_amount"],
                    reserved_amount=row["reserved_amount"],
                    warehouse=warehouse
                )

            if len(raw_data['result']['rows']) != body['limit'] + body['offset']:
                break
            else:
                body['offset'] += body['limit']
