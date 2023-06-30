"""Прогнозирования остатков на складе
"""
import math
from datetime import timedelta

from strite_data_hub.dataclasses import PredictionFOS, PredictionFOF


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
    :param avg_delivery_time:  (Tc) время от наступления точки заказа, времени на сборку, времени доставки на склад и приемки на складе (дни) See for ozon: https://docs.ozon.ru/retail/contract/komissions/
    :param avg_consumption: (Сред расход) средний расход в день
    :param deviation_sales: (Срасхода) среднеквадратичное отклонение расхода запаса(продаж)
    :param time_delta: Интервал времени контроля (дни)
    :param integral: (Xp) Значение интегральной функции лапласа для нормального распределения (табличное значение лапласа для 95% = 1.645)
    :param deviation_delivery_time: (Cc) среднеквадратичное отклонение времени выполнения доставки
    :return: PredictionFOS
    """
    result = PredictionFOS()

    _d_adt = avg_delivery_time.total_seconds()/timedelta(days=1).total_seconds()
    _d_delta = time_delta.total_seconds()/timedelta(days=1).total_seconds()

    result.safety_stock = integral * math.sqrt(
        (_d_adt + _d_delta) * math.pow(deviation_sales, 2) +
        avg_consumption * math.pow(deviation_delivery_time, 2)
    )

    result.max_stock = result.safety_stock + size_supply
    result.order_point = avg_consumption * _d_adt + result.safety_stock
    result.average_stock_level = size_supply/2 + result.safety_stock

    return result


def get_basic_predication_supplies_fof(size_supply: int,
                                       avg_consumption_per_day: float,
                                       consumption: int,
                                       period: timedelta,
                                       avg_delivery_time: timedelta,
                                       deviation_sales: float,
                                       current_stock: int) -> PredictionFOF:
    """Расчет объема поставок
    :param size_supply: оптимальный размер поставки
    :param avg_consumption_per_day: Средняя интенсивность потребления товаров
    :param consumption: расход товара за период
    :param period: период
    :param avg_delivery_time:  (Tc) время от наступления точки заказа, времени на сборку, времени доставки на склад и приемки на складе (дни) See for ozon: https://docs.ozon.ru/retail/contract/komissions/
    :param deviation_sales: (Срасхода) среднеквадратичное отклонение расхода запаса(продаж)
    :param current_stock: текущий запас

    :return: PredictionFOF
    """
    result = PredictionFOF()

    # Время отправления заказа
    result.order_date = timedelta(
        days=(period.total_seconds()/timedelta(days=1).total_seconds())-current_stock/avg_consumption_per_day
    )

    result.safety_stock = 1.645 * deviation_sales * math.sqrt(result.order_date.days*avg_delivery_time.days)

    result.current_stock_date = timedelta(days=avg_consumption_per_day*(result.order_date.total_seconds()/timedelta(days=1).total_seconds()+avg_delivery_time.total_seconds()/timedelta(days=1).total_seconds()))

    result.max_stock = result.safety_stock + size_supply

    return result
