import logging
from dataclasses import dataclass
from typing import Self, Optional, Literal
from datetime import datetime
from .api import wb_request
from .products import WbProduct


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

    def get_product(self, api_data: dict):
        """
        Загружает информацию о товаре
        :param api_data:
        :return:
        """
        search_result = WbProduct.get_products_by_codes(api_data, [self.vendor_code])
        self.product = next(iter(item for item in search_result if item.vendor_code == self.vendor_code), None)

    @classmethod
    def get_list_products(cls, api_data: dict, orders: list[Self]):
        """
        Загружает информацию о товарах
        :param api_data:
        :param orders:
        :return:
        """
        search_result = WbProduct.get_products_by_codes(api_data, [item.vendor_code for item in orders])
        for item in orders:
            item.product = next(iter(_item for _item in search_result if _item.vendor_code == item.vendor_code), None)

    def cancel(self, api_data: dict) -> bool:
        try:
            wb_request(f"https://suppliers-api.wildberries.ru/api/v3/orders/{self.id}/cancel",
                       api_data,
                       version="new",
                       method="PATCH")
        except Exception as e:
            logging.error(f"Error while canceling order {self.id}: {e}")
            return False
        return True

    def get_sticker(self, api_data: dict):
        raw_data = wb_request('https://suppliers-api.wildberries.ru/api/v3/orders/stickers',
                              api_data,
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
    def get_new_orders(cls, api_data: dict) -> list[Self]:
        raw_data = wb_request('https://suppliers-api.wildberries.ru/api/v3/orders/new',
                              api_data,
                              version="new",
                              method="GET")

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

    def get_orders(self, api_data: dict) -> list[WbOrder]:
        raw_data = wb_new_get(f"https://suppliers-api.wildberries.ru/api/v3/supplies/{self.id}/orders",
                              api_data['marketplace'], None)

        for _o in raw_data['orders']:
            yield WbOrder.parse_from_dict({**_o, 'deliveryType': 'fbs'})

    def add_order(self, api_data: dict, order_id: int, test: bool = False) -> bool:
        if not test:
            wb_new_patch(f"https://suppliers-api.wildberries.ru/api/v3/supplies/{self.id}/orders/{order_id}",
                         api_data['marketplace'], None, None)
        return True

    def close(self, api_data: dict, test: bool = False) -> bool:
        if not test:
            wb_new_patch(f"https://suppliers-api.wildberries.ru/api/v3/supplies/{self.id}/deliver",
                         api_data['marketplace'], None, None)
        return True

    def cancel(self, api_data: dict, test: bool = False) -> bool:
        if not test:
            wb_new_patch(f"https://suppliers-api.wildberries.ru/api/v3/supplies/{self.id}/cancel",
                         api_data['marketplace'], None, None)
        return True

    def delete(self, api_data: dict):
        wb_new_delete(f"https://suppliers-api.wildberries.ru/api/v3/supplies/{self.id}", api_data['marketplace'], None)
        return True

    @classmethod
    def get_supplies(cls, api_data: dict) -> list[Self]:
        query = {
            "limit": 50,
            "next": 0
        }

        while True:
            raw_data = wb_new_get("https://suppliers-api.wildberries.ru/api/v3/supplies", api_data['marketplace'],
                                  query)

            for s_data in raw_data['supplies']:
                yield cls.parse_from_dict(s_data)

            if len(raw_data['supplies']) < query['limit']:
                break
            else:
                query['next'] = raw_data['next']

    @classmethod
    def get_supply_by_id(cls, api_data: dict, supply_id: str) -> Self:
        raw_data = wb_new_get(f'https://suppliers-api.wildberries.ru/api/v3/supplies/{supply_id}',
                              api_data['marketplace'], None)
        return cls.parse_from_dict(raw_data)

    @classmethod
    def create_supply(cls, api_data: dict, name: str) -> Self:
        raw_data = wb_new_post("https://suppliers-api.wildberries.ru/api/v3/supplies", api_data['marketplace'], None,
                               {'name': name})
        return cls.get_supply_by_id(api_data, raw_data['id'])
