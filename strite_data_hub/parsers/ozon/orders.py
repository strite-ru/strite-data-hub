from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self, Optional, Literal, List

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
    orderId: str  # order_number
    postingNumber: str  # posting_number
    status: Literal['awaiting_packaging', 'awaiting_deliver', 'delivering', 'delivered', 'cancelled']
    orders: list[OzonOrder]
    processTo: datetime


@dataclass(frozen=True)
class OzonFBOPosting(OzonPosting):
    """
    Данные по отправлению FBO
    """
    warehouseFromId: int
    warehouseFromName: str
    warehouseToRegion: str

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        return cls(
            orderId=raw_data['order_number'],
            postingNumber=raw_data['posting_number'],
            processTo=datetime.strptime(raw_data['in_process_at'][:16], '%Y-%m-%dT%H:%M') if raw_data.get(
                'in_process_at', None) else None,
            orders=[OzonOrder(price=float(_o['price']), vendor_code=_o['offer_id'], sku=_o['sku'],
                              quantity=_o['quantity'])
                    for _o in raw_data['products']],
            status=raw_data['status'],
            warehouseFromId=raw_data['analytics_data']['warehouse_id'],
            warehouseFromName=raw_data['analytics_data']['warehouse_name'],
            warehouseToRegion=raw_data['analytics_data']['region']
        )

    def to_dict(self) -> dict:
        return {
            "order_number": self.orderId,
            "posting_number": self.postingNumber,
            "in_process_at": self.processTo.strftime('%Y-%m-%dT%H:%M:%SZ') if self.processTo else None,
            "products": [
                {
                    "price": _o.price,
                    "offer_id": _o.vendor_code,
                    "sku": _o.sku,
                    "quantity": _o.quantity
                }
                for _o in self.orders
            ],
            "status": self.status,
            "warehouse_id": self.warehouseFromId,
        }

    @classmethod
    def get_postings(cls,
                     api: OzonAPI,
                     status: Optional[Literal['awaiting_packaging', 'awaiting_deliver', 'delivering', 'delivered', 'cancelled']],
                     date_from: datetime = datetime.now() - timedelta(days=15),
                     date_to: datetime = datetime.now()) -> List[Self]:
        """
        Получение списка отправлений по статусу в Ozon
        :param api:
        :param status:
        :param date_from:
        :param date_to:
        :return:
        """
        body = {
            "dir": "ASC",
            "filter": {
                "since": f"{date_from.date()}T00:00:00Z",
                "status": status,
                "to": f"{date_to.date()}T23:59:59Z"
            },
            "limit": 100,
            "offset": 0,
            "translit": False,
            "with": {
                "analytics_data": True,
                "financial_data": False
            }
        }

        while True:
            raw_data: dict = api.request(url="v2/posting/fbo/list",
                                   method="POST",
                                   json=body)

            if 'result' not in raw_data.keys():
                err = Exception(f"Не смогли получить список заказов магазина Ozon: {raw_data}")
                logger.error(err)
                raise err

            for _p in raw_data['result']:
                yield cls.parse_from_dict(_p)

            if len(raw_data['result']) == body['limit']:
                body['offset'] += body['limit']
            else:
                break


@dataclass(frozen=True)
class OzonFBSPosting(OzonPosting):
    barcode: Optional[str]  # barcodes.lower_barcode
    shipmentAt: Optional[datetime]
    deliverAt: Optional[datetime]
    warehouseToId: int

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        return cls(
            orderId=raw_data['order_number'],
            postingNumber=raw_data['posting_number'],
            barcode=raw_data['barcodes']['lower_barcode'] if raw_data.get('barcodes', None) else None,
            processTo=datetime.strptime(raw_data['in_process_at'][:16], '%Y-%m-%dT%H:%M') if raw_data.get(
                'in_process_at', None) else None,
            shipmentAt=datetime.strptime(raw_data['shipment_date'][:16], '%Y-%m-%dT%H:%M') if raw_data.get(
                'shipment_date', None) else None,
            deliverAt=datetime.strptime(raw_data['delivering_date'][:16], '%Y-%m-%dT%H:%M') if raw_data.get(
                'delivering_date', None) else None,
            orders=[OzonOrder(price=float(_o['price']), vendor_code=_o['offer_id'], sku=_o['sku'],
                              quantity=_o['quantity'])
                    for _o in raw_data['products']],
            status=raw_data['status'],
            warehouseToId=raw_data['analytics_data']['warehouse_id'] if raw_data.get('analytics_data', None) else None
        )

    def to_dict(self) -> dict:
        return {
            "order_number": self.orderId,
            "posting_number": self.postingNumber,
            "in_process_at": self.processTo.strftime('%Y-%m-%dT%H:%M:%SZ') if self.processTo else None,
            "products": [
                {
                    "price": _o.price,
                    "offer_id": _o.vendor_code,
                    "sku": _o.sku,
                    "quantity": _o.quantity
                }
                for _o in self.orders
            ],
            "status": self.status,
            "warehouse_id": self.warehouseToId,
        }

    @classmethod
    def get_postings(cls,
                        api: OzonAPI,
                        status: Optional[Literal['awaiting_packaging', 'awaiting_deliver', 'delivering', 'delivered', 'cancelled']],
                        date_from: datetime = datetime.now() - timedelta(days=15),
                        date_to: datetime = datetime.now()) -> List[Self]:
        """
        Получение списка отправлений по статусу в Ozon
        :param api:
        :param status:
        :param date_from:
        :param date_to:
        :return:
        """
        body = {
            "dir": "ASC",
            "filter": {
                "since": f"{date_from.date()}T00:00:00Z",
                "to": f"{date_to.date()}T23:59:59Z",
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
            "posting_number": self.postingNumber
        }
        api.request(url="v3/posting/fbs/ship", json=body)

    def get_sticker(self, api: OzonAPI) -> bytes:
        body = {
            "posting_number": [self.postingNumber]
        }
        return api.request(url="v2/posting/fbs/package-label",
                           content_type="application/pdf",
                           json=body)
