from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Self, Optional


@dataclass()
class PredictionFOS:
    """Фиксированный размер заказа
    """
    safety_stock: float = 0
    max_reserve: float = 0
    order_point: float = 0
    average_stock_level: float = 0



