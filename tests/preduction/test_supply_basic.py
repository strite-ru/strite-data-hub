from strite_data_hub.prediction.supplies.basic import get_basic_predication_supplies_fos

from datetime import timedelta


def test_basic_prediction():
    result = get_basic_predication_supplies_fos(size_supply=90,
                                                avg_delivery_time=timedelta(days=6),
                                                deviation_delivery_time=1,
                                                deviation_sales=6.0,
                                                avg_consumption=3.0)

    assert result.safety_stock == 24.34377692553068
    assert result.max_reserve == 114.34377692553068
    assert result.order_point == 42.343776925530676
    assert result.average_stock_level == 69.34377692553068
