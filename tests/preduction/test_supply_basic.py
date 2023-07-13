from strite_data_hub.prediction.supplies.basic import get_basic_predication_supplies_fos, \
    get_basic_predication_supplies_fof

from datetime import timedelta


def test_basic_prediction_fos():
    result = get_basic_predication_supplies_fos(current_stock=50,
                                                avg_consumption=3.0,
                                                deviation_sales=6.0,
                                                size_supply=30,
                                                supply_delivery_time=timedelta(days=3))

    assert result.safety_stock == 19.113172813533602
    assert result.max_stock == 49.1131728135336
    assert result.order_point == 28.113172813533602
    assert result.supply_date.days == 7
    assert result.average_stock_level == 34.1131728135336


def test_basic_prediction_fof():
    result = get_basic_predication_supplies_fof(current_stock=50,
                                                avg_consumption=3.0,
                                                deviation_sales=6.0,
                                                supply_delivery_time=timedelta(days=3),
                                                period=timedelta(days=7))

    assert result.safety_stock == 60.03686617404343
    assert result.max_stock == 90.03686617404344
    assert result.supply_date.days == 6
    assert result.supply_size == 30
    assert result.average_stock_level == 75.03686617404344
