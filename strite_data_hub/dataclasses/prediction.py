from dataclasses import dataclass
from datetime import timedelta


@dataclass()
class PredictionFOS:
    """Фиксированный размер заказа

    Attributes:
        safety_stock:        Страховой запас
        max_stock:           Максимальный запас
        order_point:         Точка заказа
        supply_date:         Дата поставки
        average_stock_level: Средний уровень запаса
    """
    safety_stock: float = 0
    max_stock: float = 0
    order_point: float = 0
    supply_date: timedelta = timedelta(days=0)
    average_stock_level: float = 0


@dataclass()
class PredictionFOF:
    """Фиксированная периодичность заказа

    Attributes:
        safety_stock:        Страховой запас
        max_stock:           Максимальный запас
        supply_size:         Размер заказа
        supply_date:         Дата поставки
        average_stock_level: Средний уровень запаса
    """
    safety_stock: int = 0
    max_stock: int = 0
    supply_size: int = 0
    supply_date: timedelta = timedelta(days=0)
    average_stock_level: float = 0
