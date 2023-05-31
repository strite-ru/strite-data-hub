from dataclasses import dataclass
from datetime import timedelta


@dataclass()
class PredictionFOS:
    """Фиксированный размер заказа

    Attributes:
        safety_stock:        Страховой запас
        max_stock:           Максимальный запас
        order_point:         Точка заказа
        average_stock_level: Средний уровень запаса
    """
    safety_stock: float = 0
    max_stock: float = 0
    order_point: float = 0
    average_stock_level: float = 0


@dataclass()
class PredictionFOF:
    """Фиксированная периодичность заказа

    Attributes:
        safety_stock:        Страховой запас
        max_stock:           Максимальный запас
        order_date:          Периодичность заказа
        current_stock_date:  Текущий запас (дней)
    """
    safety_stock: float = 0
    max_stock: float = 0
    order_date: timedelta = timedelta(days=0)
    current_stock_date: timedelta = timedelta(days=0)
