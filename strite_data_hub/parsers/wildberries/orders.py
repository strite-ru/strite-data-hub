from dataclasses import dataclass
from typing import Self, Optional, Literal
from datetime import datetime
from .api import WildberriesAPI
from .products import WbProduct
import logging

logger = logging.getLogger("Strite")


@dataclass(frozen=True)
class WbSticker:
    orderId: int  # WbOrder.id
    partA: int
    partB: int
    barcode: str

    def __dict__(self) -> dict:
        return {
            "orderId": self.orderId,
            "partA": self.partA,
            "partB": self.partB,
            "barcode": self.barcode
        }


@dataclass()
class WbOrder:
    deliveryType: Literal['fbs', 'dbs']  # Тип доставки: fbs - доставка на склад, dbs - доставка силами поставщика.
    vendor_code: str
    chartId: int
    orderId: str  # orderUId
    id: int
    rid: str  # rid
    createdAt: datetime
    warehouseId: int
    supplyId: Optional[str]
    barcode: list[str]  # skus
    price: int  # price
    product: Optional[WbProduct] = None
    sticker: Optional[WbSticker] = None

    def get_product(self, api: WildberriesAPI):
        """
        Загружает информацию о товаре
        :param api:
        :return:
        """
        search_result = WbProduct.get_products_by_codes(api, [self.vendor_code])
        self.product = next(iter(item for item in search_result if item.vendor_code == self.vendor_code), None)

    @classmethod
    def get_list_products(cls, api: WildberriesAPI, orders: list[Self]):
        """
        Загружает информацию о товарах
        :param api:
        :param orders:
        :return:
        """
        search_result = WbProduct.get_products_by_codes(api, [item.vendor_code for item in orders])
        for item in orders:
            item.product = next(iter(_item for _item in search_result if _item.vendor_code == item.vendor_code), None)

    def cancel(self, api: WildberriesAPI) -> None:
        try:
            api.marketplace_request(url=f"api/v3/orders/{self.id}/cancel", method="PATCH")
        except Exception as e:
            logger.error(msg := f"Error while canceling order {self.id}: {e}")
            raise Exception(msg)

    def get_sticker(self, api: WildberriesAPI):
        raw_data = api.marketplace_request(url="api/v3/orders/stickers",
                                           method="POST",
                                           params={'type': 'svg', 'width': 58, 'height': 40},
                                           body={'orders': [self.id]})
        if len(raw_data['stickers']) > 0:
            del raw_data['stickers'][0]['file']
            self.sticker = WbSticker(orderId=self.id, **raw_data['stickers'][0])

    @classmethod
    def parse_from_dict(cls, raw_item: dict) -> Self:
        return cls(
            id=raw_item['id'],
            rid=raw_item['rid'],
            orderId=raw_item['orderUid'],
            createdAt=datetime.strptime(raw_item['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
            warehouseId=raw_item['warehouseId'],
            supplyId=raw_item.get('supplyId'),
            barcode=raw_item['skus'],
            price=raw_item['price'] / 100,
            vendor_code=raw_item['article'],
            chartId=raw_item['chrtId'],
            deliveryType=raw_item['deliveryType']
        )

    def __dict__(self):
        return {
            'id': self.id,
            'rid': self.rid,
            'orderId': self.orderId,
            'createdAt': self.createdAt,
            'warehouseId': self.warehouseId,
            'supplyId': self.supplyId,
            'barcode': self.barcode,
            'price': self.price,
            'vendor_code': self.vendor_code,
            'chartId': self.chartId,
            'deliveryType': self.deliveryType
        }

    @classmethod
    def get_new_orders(cls, api: WildberriesAPI) -> list[Self]:
        raw_data = api.marketplace_request(url="api/v3/orders/new")

        for _o in raw_data['orders']:
            yield cls.parse_from_dict(_o)


@dataclass()
class WbSupply:
    id: str
    done: bool
    name: str
    createdAt: datetime
    scanAt: Optional[datetime]  # scanDt
    closedAt: Optional[datetime]
    orders: Optional[list[WbOrder]] = None

    @classmethod
    def parse_from_dict(cls, raw_item: dict) -> Self:
        return cls(
            id=raw_item['id'],
            name=raw_item['name'],
            createdAt=datetime.strptime(raw_item['createdAt'], '%Y-%m-%dT%H:%M:%SZ'),
            scanAt=datetime.strptime(raw_item['scanDt'], '%Y-%m-%dT%H:%M:%SZ') if raw_item['scanDt'] else None,
            closedAt=datetime.strptime(raw_item['closedAt'], '%Y-%m-%dT%H:%M:%SZ') if raw_item['closedAt'] else None,
            done=raw_item['done']
        )

    def get_orders(self, api: WildberriesAPI) -> list[WbOrder]:
        raw_data = api.marketplace_request(url=f"api/v3/supplies/{self.id}/orders")

        for _o in raw_data['orders']:
            yield WbOrder.parse_from_dict({**_o, 'deliveryType': 'fbs'})

    def add_order(self, api: WildberriesAPI, order_id: int) -> None:
        api.marketplace_request(url=f"api/v3/supplies/{self.id}/orders/{order_id}", method="PATCH")

    def close(self, api: WildberriesAPI) -> None:
        api.marketplace_request(url=f"api/v3/supplies/{self.id}/deliver", method="PATCH")

    def cancel(self, api: WildberriesAPI) -> None:
        api.marketplace_request(url=f"api/v3/supplies/{self.id}/cancel", method="PATCH")

    def delete(self, api: WildberriesAPI) -> None:
        api.marketplace_request(url=f"api/v3/supplies/{self.id}", method="DELETE")

    @classmethod
    def get_supplies(cls, api: WildberriesAPI) -> list[Self]:
        query = {
            "limit": 50,
            "next": 0
        }

        while True:
            raw_data = api.marketplace_request(url="api/v3/supplies", params=query)

            for s_data in raw_data['supplies']:
                yield cls.parse_from_dict(s_data)

            if len(raw_data['supplies']) < query['limit']:
                break
            else:
                query['next'] = raw_data['next']

    @classmethod
    def get_supply_by_id(cls, api: WildberriesAPI, supply_id: str) -> Self:
        return cls.parse_from_dict(api.marketplace_request(url=f"api/v3/supplies/{supply_id}"))

    @classmethod
    def create_supply(cls, api: WildberriesAPI, name: str) -> Self:
        raw_data = api.marketplace_request(url="api/v3/supplies", method="POST", body={'name': name})
        return cls.get_supply_by_id(api, raw_data["id"])
