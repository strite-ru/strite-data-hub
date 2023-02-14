from dataclasses import dataclass
from typing import Self

from .api import wb_request


@dataclass(frozen=True)
class WbWarehouse:
    name: str
    id: int

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        return cls(
            name=raw_data['name'],
            id=raw_data['id']
        )

    @classmethod
    def get_warehouses(cls, api_data: dict) -> list[Self]:
        raw_data = wb_request("https://suppliers-api.wildberries.ru/api/v2/warehouses", api_data,
                              method="GET", version="new")

        for _d in raw_data:
            yield cls.parse_from_dict(_d)

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "id": self.id
        }
