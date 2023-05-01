"""Прогнозирования остатков на складе
"""
import math
from datetime import timedelta, datetime

from strite_data_hub.dataclasses import PredictionFOS, Product


def get_basic_predication_supplies_fos(size_supply: int,
                                       avg_delivery_time: timedelta,
                                       deviation_delivery_time: float,
                                       deviation_sales: float,
                                       avg_consumption: float,
                                       time_delta: timedelta = timedelta(days=0),
                                       integral: float = 1.645,
                                       ) -> PredictionFOS:
    """Расчет объема поставок
    :param size_supply: оптимальный размер поставки
    :param avg_delivery_time:  (Tc) время от наступления точки заказа, времени на сборку, времени доставки на склад и приемки на складе (дни)
    :param avg_consumption: (Сред расход) средний расход в день
    :param deviation_sales: (Срасхода) среднеквадратичное отклонение расхода запаса(продаж)
    :param time_delta: Интервал времени контроля (дни)
    :param integral: (Xp) Значение интегральной функции лапласа для нормального распределения (табличное значение лапласа для 95% = 1.645)
    :param deviation_delivery_time: (Cc) среднеквадратичное отклонение времени выполнения доставки
    :return: PredictionFOS
    """
    result = PredictionFOS()

    _d_adt = avg_delivery_time.total_seconds()/timedelta(days=1).total_seconds()

    result.safety_stock = integral * math.sqrt(
        _d_adt * math.pow(deviation_sales, 2) +
        avg_consumption * math.pow(deviation_delivery_time, 2)
    )

    result.max_reserve = result.safety_stock + size_supply
    result.order_point = avg_consumption * _d_adt + result.safety_stock
    result.average_stock_level = size_supply/2 + result.safety_stock

    return result
