from dataclasses import dataclass
from typing import Self, Optional, Any

from .api import WildberriesAPI


@dataclass(frozen=True)
class WbChart:
    """
    Объект хранения размеров
    """
    id: Optional[int]  # chrtID
    skus: list[str]  # Массив баркодов
    name: str  # techSize Размер поставщика
    price: Optional[int]  # price

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        """
        Парсинг данных из json
        Reference: https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1cursor~1list/post
        :param raw_data: данные в формате json
        :return: WbChart
        """
        return cls(
            id=raw_data.get('chrtID', None),
            skus=raw_data['skus'],
            name=raw_data['techSize'],
            price=raw_data.get('price', None)
        )

    def __dict__(self) -> dict:
        return {
            "id": self.id,
            "skus": self.skus,
            "name": self.name,
            "price": self.price
        }


@dataclass(frozen=True)
class WbCharacteristic:
    """
    Объект хранения характеристик
    """
    key: list[str]
    value: Any

    def __dict__(self) -> dict:
        return {
            "key": self.key,
            "value": self.value
        }

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        """
        Парсинг данных из json
        Reference: https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1cursor~1list/post
        :param raw_data: данные в формате json
        :return: WbCharacteristic
        """
        return cls(
            key=next(iter(raw_data)),
            value=raw_data[next(iter(raw_data))]
        )


@dataclass(frozen=True)
class WbProduct:
    """
    Объект хранения товара
    """
    id: int  # nmID
    name: Optional[str]  # none
    sizes: list[WbChart]  # sizes
    images: list[str]  # mediaFiles
    vendor_code: str  # vendorCode
    link: str  # generate
    brand: Optional[str]  # brand
    category: Optional[str]  # object
    characteristics: Optional[list[WbCharacteristic]]

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        """
        Парсинг данных из json
        Reference: https://openapi.wb.ru/#tag/Kontent-Prosmotr/paths/~1content~1v1~1cards~1cursor~1list/post
        :param raw_data: данные в формате json
        :return: WbProduct
        """

        if name := next((item for item in raw_data.get("characteristics", []) if item.get("Наименование")), None):
            raw_data["name"] = name['Наименование']
        if brand := next((item for item in raw_data.get("characteristics", []) if item.get("Бренд")), None):
            raw_data["brand"] = brand['Бренд']
        if category := next((item for item in raw_data.get("characteristics", []) if item.get("Предмет")), None):
            raw_data["object"] = category['Предмет']

        return cls(
            id=raw_data['nmID'],
            name=raw_data.get("name", None),
            brand=raw_data.get("brand", None),
            category=raw_data.get("object", None),
            vendor_code=raw_data['vendorCode'],
            sizes=[WbChart.parse_from_dict(_s) for _s in raw_data['sizes']],
            link=f"https://www.wildberries.ru/catalog/{raw_data['nmID']}/detail.aspx",  # Генерация ссылки
            images=raw_data['mediaFiles'],  # Первое изображение массива изображений товара
            characteristics=[WbCharacteristic.parse_from_dict(_c) for _c in raw_data.get("characteristics", [])]
        )

    def __dict__(self):
        return {
            'id': self.id,
            'name': self.name,
            'sizes': self.sizes,
            'images': self.images,
            'vendor_code': self.vendor_code,
            'link': self.link,
            'brand': self.brand,
            'category': self.category,
            "characteristics": self.characteristics
        }

    @classmethod
    def get_products(cls, api: WildberriesAPI) -> list[Self]:
        """
        Получение списка товаров из Wildberries
        :param api: доступы к API
        :return: список товаров
        """
        # Тело запроса
        body = {
            "sort": {
                "cursor": {
                    # "updatedAt": None,
                    # "nmID": None,
                    "limit": 10
                },
                "filter": {
                    "withPhoto": -1
                },
                "sort": {
                    "sortColumn": "updateAt",
                    "ascending": False
                }
            }
        }

        while True:
            raw_data = api.marketplace_request(url="content/v1/cards/cursor/list", method="POST", json=body)

            # Возвращаем список товаров
            yield from (cls.parse_from_dict(_p) for _p in raw_data['data']['cards'])

            # Если товаров меньше чем лимит, то выходим из цикла
            if len(raw_data['data']['cards']) < body['sort']['cursor']['limit']:
                break
            # Иначе обновляем курсор
            body['sort']['cursor']['updatedAt'] = raw_data['data']['cursor']['updatedAt']
            body['sort']['cursor']['nmID'] = raw_data['data']['cursor']['nmID']

    @classmethod
    def get_products_by_codes(cls, api: WildberriesAPI, vendor_codes: list[str]):
        def divide_chunks(l, n):
            for i in range(0, len(l), n):
                yield l[i:i + n]

        for codes in divide_chunks(vendor_codes, 100):
            raw_data = api.marketplace_request(url="content/v1/cards/filter",
                                               method="POST",
                                               json={
                                                   "vendorCodes": codes
                                               })
            yield from (cls.parse_from_dict(_p) for _p in raw_data['data'])

    def update_stock_balance(self, api: WildberriesAPI, new_stock_value: int):
        """Обновление (измение) числа товара на маркетплейсе"""
        pass
