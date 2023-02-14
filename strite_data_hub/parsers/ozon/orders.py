from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self, Optional, Literal

from .api import ozon_request
from .products import OzonProduct


@dataclass(frozen=True)
class OzonOrder:
    price: float
    vendor_code: str
    sku: int
    quantity: int

    def get_product_info(self, api_data: dict) -> OzonProduct:
        _products = list(OzonProduct.get_products_by_codes(api_data, [self.vendor_code]))
        if len(_products) == 0:
            raise Exception(f"Не смогли получить информацию о товаре {self.vendor_code}")
        for item in _products:
            if item is None:
                continue
            if item.vendor_code == self.vendor_code:
                return item
        raise Exception(f"Не смогли получить информацию о товаре {self.vendor_code}")

    @classmethod
    def get_products_info(cls, api_data: dict, orders: list[Self]) -> list[OzonProduct]:
        _products = list(OzonProduct.get_products_by_codes(api_data, [o.vendor_code for o in orders]))
        if len(_products) == 0:
            raise Exception(f"Не смогли получить информацию о товарах {', '.join([o.vendor_code for o in orders])}")
        for item in _products:
            if item is None:
                continue
            for order in orders:
                if item.vendor_code == order.vendor_code:
                    yield item


@dataclass(frozen=True)
class OzonPosting:
    """
    Данные по отправлению
    """

    orderId: str  # order_number
    postingId: str  # posting_number
    barcode: str  # barcodes.lower_barcode
    processTo: datetime
    shipmentAt: Optional[datetime]
    deliverAt: Optional[datetime]
    orders: list[OzonOrder]
    status: str

    def close(self, api_data: dict, test: bool = False) -> bool:
        if not test:
            def to_dict(value: OzonOrder) -> dict:
                return {
                    "exemplar_info": [
                        {
                            "is_gtd_absent": True
                        }
                    ],
                    "product_id": value.sku,
                    "quantity": value.quantity
                }

            body = {
                "packages": [
                    {
                        "products": [to_dict(_o) for _o in self.orders],
                    }
                ],
                "posting_number": self.postingId
            }
            ozon_request("https://api-seller.ozon.ru/v3/posting/fbs/ship", api_data, body=body)
        return True

    def get_sticker(self, api_data: dict) -> bytes:
        body = {
            "posting_number": [self.postingId]
        }
        return ozon_request("https://api-seller.ozon.ru/v2/posting/fbs/package-label",
                            api_data,
                            content_type="application/pdf",
                            body=body)

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        return cls(
            orderId=raw_data['order_number'],
            postingId=raw_data['posting_number'],
            barcode=raw_data['barcodes']['lower_barcode'],
            processTo=datetime.strptime(raw_data['in_process_at'], '%Y-%m-%dT%H:%M:%SZ'),
            shipmentAt=datetime.strptime(raw_data['shipment_date'], '%Y-%m-%dT%H:%M:%SZ') if raw_data[
                'shipment_date'] else None,
            deliverAt=datetime.strptime(raw_data['delivering_date'], '%Y-%m-%dT%H:%M:%SZ') if raw_data[
                'delivering_date'] else None,
            orders=[OzonOrder(price=float(_o['price']), vendor_code=_o['offer_id'], sku=_o['sku'],
                              quantity=_o['quantity'])
                    for _o in raw_data['products']],
            status=raw_data['status']
        )

    @classmethod
    def create_act(cls, api_data: dict, departure_date: datetime, test: bool = False) -> bool:
        if not test:
            body = {
                "departure_date": departure_date.strftime('%Y-%m-%dT%H:%M:%SZ')
            }
            ozon_request("https://api-seller.ozon.ru/v2/posting/fbs/act/create", api_data, body=body)
        return True

    @classmethod
    def get_postings(cls, api_data: dict,
                     status: Optional[Literal['awaiting_packaging', 'awaiting_deliver', 'delivering']]) -> list[Self]:
        """
        Получение списка отправлений по статусу в Ozon
        :param api_data: данные для авторизации
        :param status: статус отправления
        :return:
        """
        body = {
            "dir": "ASC",
            "filter": {
                "since": f"{(datetime.now() - timedelta(days=15)).date()}T00:00:00Z",
                "to": f"{datetime.now().date()}T23:59:59Z",
            },
            "limit": 500,
            "offset": 0,
            "with": {
                "analytics_data": False,
                "barcodes": True,
                "financial_data": False,
                "translit": False
            }
        }
        if status:
            body['filter']['status'] = status

        while True:
            raw_data = ozon_request("https://api-seller.ozon.ru/v3/posting/fbs/list", api_data, body=body)

            if not raw_data.get('result', None):
                raise Exception("Не смогли получить список заказов магазина Ozon")

            for _p in raw_data['result']['postings']:
                yield cls.parse_from_dict(_p)

            if raw_data['result']['has_next']:
                body['offset'] += body['limit']
            else:
                break
