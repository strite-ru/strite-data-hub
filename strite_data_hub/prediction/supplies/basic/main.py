"""Прогнозирования остатков на складе
"""
import datetime
import math
from datetime import timedelta

from strite_data_hub.dataclasses import PredictionFOS, PredictionFOF


def get_basic_predication_supplies_fos(current_stock: int,
                                       avg_consumption: float,
                                       deviation_sales: float,
                                       size_supply: int,
                                       supply_delivery_time: timedelta,
                                       integral: float = 1.645) -> PredictionFOS:
    """Расчет объема поставок
    :param supply_delivery_time: Время на обработку заказа и доставку
    :param current_stock: Текущий остаток на складе
    :param size_supply: Оптимальный размер поставки
    :param avg_consumption: (Сред расход) средний расход в день
    :param deviation_sales: (Срасхода) среднеквадратичное отклонение расхода запаса(продаж)
    :param integral: (Xp) Значение интегральной функции лапласа для нормального распределения (табличное значение лапласа для 95% = 1.645)
    :return: PredictionFOS
    """
    result = PredictionFOS()

    _d_sdt = supply_delivery_time.total_seconds()/timedelta(days=1).total_seconds()

    result.safety_stock = integral * math.sqrt(_d_sdt * math.pow(deviation_sales, 2) +
                                               avg_consumption * math.pow(supply_delivery_time.days, 2))

    result.max_stock = result.safety_stock + size_supply
    result.order_point = avg_consumption * _d_sdt + result.safety_stock
    result.supply_date = timedelta(days=(current_stock - result.order_point) / avg_consumption)
    result.average_stock_level = size_supply/2 + result.safety_stock

    return result


def get_basic_predication_supplies_fof(current_stock: int,
                                       avg_consumption: float,
                                       deviation_sales: float,
                                       supply_delivery_time: timedelta,
                                       period: timedelta = timedelta(days=30),
                                       integral: float = 1.645) -> PredictionFOF:
    """Расчет объема поставок
    :param current_stock: Текущий остаток на складе
    :param avg_consumption: (Сред расход) средний расход в день
    :param deviation_sales: (Срасхода) среднеквадратичное отклонение расхода запаса(продаж)
    :param supply_delivery_time: Время на обработку заказа и доставку
    :param period: Период поставок
    :param integral: (Xp) Значение интегральной функции лапласа для нормального распределения (табличное значение лапласа для 95% = 1.645)
    :return: PredictionFOF
    """
    result = PredictionFOF()

    _d_p = period.total_seconds() / timedelta(days=1).total_seconds()
    _d_sdt = supply_delivery_time.total_seconds() / timedelta(days=1).total_seconds()

    result.safety_stock = integral * deviation_sales * math.sqrt(_d_sdt + _d_p + avg_consumption * math.pow(supply_delivery_time.days, 2))
    result.supply_size = avg_consumption * (_d_sdt + _d_p)
    result.max_stock = result.safety_stock + result.supply_size
    days = (current_stock - result.supply_size) / avg_consumption
    result.supply_date = timedelta(days=days)
    result.average_stock_level = result.supply_size/2 + result.safety_stock

    return result
