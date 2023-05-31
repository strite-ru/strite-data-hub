from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self, Optional, Literal

from .api import OzonAPI
from .products import OzonProduct
import logging

logger = logging.getLogger("Strite")


@dataclass(frozen=True)
class OzonOrder:
    price: float
    vendor_code: str
    sku: int
    quantity: int

    def get_product_info(self, products: list[OzonProduct]) -> OzonProduct:
        logger.debug(f"get_product_info ({self.vendor_code})")

        for item in products:
            if item is None:
                continue
            if item.vendor_code == self.vendor_code:
                return item

        logger.error(msg := f"Не смогли получить информацию о товаре {self.vendor_code}")
        raise Exception(msg)

    @classmethod
    def get_products_info(cls, api: OzonAPI, orders: list[Self]) -> list[OzonProduct]:
        logger.debug(f"Получение данных о товарах из маркета из заказов")

        _products = list(OzonProduct.get_products_by_codes(api, [o.vendor_code for o in orders]))

        for order in orders:
            yield order.get_product_info(_products)


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

    def close(self, api: OzonAPI) -> None:
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
        api.request(url="v3/posting/fbs/ship", json=body)

    def get_sticker(self, api: OzonAPI) -> bytes:
        body = {
            "posting_number": [self.postingId]
        }
        return api.request(url="v2/posting/fbs/package-label",
                           content_type="application/pdf",
                           json=body)

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
    def create_act(cls, api: OzonAPI, departure_date: datetime) -> bool:
        body = {
            "departure_date": departure_date.strftime('%Y-%m-%dT%H:%M:%SZ')
        }
        try:
            api.request(url="v2/posting/fbs/act/create",
                        method="POST",
                        json=body)
        except Exception as err:
            logger.error("Не удалось создать акт поставки", err)
            return False
        return True

    @classmethod
    def get_postings(cls,
                     api: OzonAPI,
                     status: Optional[Literal['awaiting_packaging', 'awaiting_deliver', 'delivering']]) -> list[Self]:
        """
        Получение списка отправлений по статусу в Ozon
        :param api:
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
            raw_data = api.request(url="v3/posting/fbs/list",
                                   method="POST",
                                   json=body)

            if not raw_data.get('result', None):
                logger.error("Не смогли получить список заказов магазина Ozon")
                raise Exception("Не смогли получить список заказов магазина Ozon")

            for _p in raw_data['result']['postings']:
                yield cls.parse_from_dict(_p)

            if raw_data['result']['has_next']:
                body['offset'] += body['limit']
            else:
                break
