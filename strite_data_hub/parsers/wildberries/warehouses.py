from dataclasses import dataclass
from typing import Self

from .api import WildberriesAPI


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
    def get_warehouses(cls, api: WildberriesAPI) -> list[Self]:
        raw_data = api.marketplace_request(url="api/v2/warehouses")

        for _d in raw_data:
            yield cls.parse_from_dict(_d)

    def __dict__(self) -> dict:
        return {
            "name": self.name,
            "id": self.id
        }
