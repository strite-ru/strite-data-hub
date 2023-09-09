from decimal import Decimal
from dataclasses import dataclass
from datetime import datetime
from typing import Self, Optional, Literal, List
from .api import OzonAPI
import logging

logger = logging.getLogger("Strite")


@dataclass(frozen=True)
class OzonSku:
    type: Literal['fbs', 'dbs', 'fbo', 'rfbs']  # source
    id: int  # sku

    @property
    def link(self):
        return f"https://www.ozon.ru/context/detail/id/{self.id}"


@dataclass(frozen=True)
class OzonProduct:
    id: int                     # id
    vendor_code: str            # offer_id
    name: str                   # name
    sizes: list[OzonSku]        # sizes
    image: str                  # primary_image
    barcode: str                # barcode
    category_id: int            # category_id

    price: Decimal              # price
    old_price: Decimal          # old_price
    currency_code: str          # currency_code

    sku: int                    # sku
    fbo_sku: Optional[int]      # fbo_sku remove
    fbs_sku: Optional[int]      # fbs_sku remove

    is_kgt: bool                # is_kgt Габаритный товар

    rating: Optional[str]       # rating

    is_discounted: bool         # is_discounted
    has_discounted_item: bool   # has_discounted_item

    created_at: datetime        # created_at
    updated_at: datetime        # updated_at

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        """
        Парсим данные о товаре из ответа Ozon
        :param raw_data: данные о товаре
        :return: объект товара
        """
        return cls(
            id=raw_data['id'],
            vendor_code=raw_data['offer_id'],
            name=raw_data['name'],
            sizes=[OzonSku(type=_s['source'], id=_s['sku']) for _s in raw_data['sources']],
            image=raw_data['primary_image'],
            barcode=raw_data['barcode'],
            category_id=raw_data['category_id'],
            price=Decimal(raw_data['price']),
            old_price=Decimal(raw_data['old_price']),
            currency_code=raw_data['currency_code'],
            sku=raw_data['sku'],
            fbo_sku=raw_data.get('fbo_sku', None),
            fbs_sku=raw_data.get('fbs_sku', None),
            is_kgt=raw_data.get('is_kgt', False),
            rating=raw_data.get('rating', None),
            is_discounted=raw_data.get('is_discounted', False),
            has_discounted_item=raw_data.get('has_discounted_item', False),
            created_at=datetime.strptime(raw_data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(raw_data['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
        )

    @classmethod
    def get_products(cls, api: OzonAPI) -> list[Self]:
        """
        Получаем список товаров магазина Ozon
        :param api: данные для авторизации
        :return: объекты товаров
        """
        body = {
            "filter": {
                "visibility": "ALL"
            },
            "last_id": "",
            "limit": 500
        }

        vendor_codes = []

        while True:
            raw_data = api.request(url="v2/product/list",
                                   method="POST",
                                   json=body)

            if not raw_data.get('result', False):
                logger.error(msg := "Не смогли получить список товаров магазина Ozon")
                raise Exception(msg)

            vendor_codes.extend([_p['offer_id'] for _p in raw_data['result']['items']])

            body['last_id'] = raw_data['result']['last_id']
            if len(vendor_codes) >= raw_data['result']['total']:
                break

        return cls.get_products_by_codes(api, vendor_codes)

    @classmethod
    def get_products_by_codes(cls, api: OzonAPI, vendor_codes: list[str]) -> list[Self]:
        """
        Получаем список товаров магазина Ozon по кодам
        :param api: данные для авторизации
        :param vendor_codes: массив кодов товаров
        :return: массив объектов товаров
        """

        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        for chunk in divide_chunks(vendor_codes, 100):
            body = {
                'offer_id': chunk
            }
            raw_product_details = api.request(url="v2/product/info/list", json=body)

            if not raw_product_details.get('result', False):
                logger.error(msg := "Не смогли получить список товаров магазина Ozon (details)")
                raise Exception(msg)

            for _p in raw_product_details['result']['items']:
                yield cls.parse_from_dict(_p)

    def update_stock_balance(self, api: OzonAPI, new_stock_value: int):
        """Обновление (измение) числа товара на маркетплейсе"""
        raise NotImplementedError

    def archive(self, api: OzonAPI):
        """Архивирование товара на маркетплейсе"""
        raise NotImplementedError

    def unarchive(self, api: OzonAPI):
        """Разархивирование товара на маркетплейсе"""
        raise NotImplementedError
