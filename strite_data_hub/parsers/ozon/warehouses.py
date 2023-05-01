"""Получение остатков товаров по сладам
"""
from dataclasses import dataclass
from typing import Self

from .api import OzonAPI


@dataclass(frozen=True)
class OzonWarehouses:
    id: str

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        pass

    @classmethod
    def get_warehouses(cls, api: OzonAPI) -> list[Self]:
        pass

    def __dict__(self) -> dict:
        return {}
