from dataclasses import dataclass


@dataclass()
class PredictionFOS:
    """Фиксированный размер заказа

    Attributes:
        safety_stock:        Страховой запас
        max_reserve:         Максимальный запас
        order_point:         Точка заказа
        average_stock_level: Средний уровень запаса
    """
    safety_stock: float = 0
    max_reserve: float = 0
    order_point: float = 0
    average_stock_level: float = 0
