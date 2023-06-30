from strite_data_hub.prediction.supplies.basic import get_basic_predication_supplies_fos, get_basic_predication_supplies_fof

from datetime import timedelta



def test_basic_prediction_fos():
    result = get_basic_predication_supplies_fos(size_supply=90,
                                                avg_delivery_time=timedelta(days=6),
                                                deviation_delivery_time=1,
                                                deviation_sales=6.0,
                                                avg_consumption=3.0)

    assert result.safety_stock == 24.34377692553068
    assert result.max_stock == 114.34377692553068
    assert result.order_point == 42.343776925530676
    assert result.average_stock_level == 69.34377692553068

def test_basic_prediction_fof():
    result = get_basic_predication_supplies_fof(size_supply=50,
                                                avg_consumption_per_day=173,
                                                consumption=527,
                                                period=timedelta(days=173),
                                                avg_delivery_time=timedelta(days=6),
                                                deviation_sales=6.0,
                                                current_stock=60)

    assert result.safety_stock == 96.70585504507987
    assert result.max_stock == 146.7058550450799
    assert result.order_date.days == 16
    assert result.current_stock_date.days == 68