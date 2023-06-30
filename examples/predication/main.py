"""
Пример использования предикативного анализа

"""
import math

from strite_data_hub.parsers.ozon.api import OzonAPI
from strite_data_hub.prediction.supplies.basic.main import get_basic_predication_supplies_fos, get_basic_predication_supplies_fof
from datetime import datetime, timedelta
from strite_data_hub.parsers.ozon.finance import OzonTransaction
from strite_data_hub.parsers.ozon.products import OzonProduct

api = OzonAPI(
    client_id=166585,
    key="58cc2e73-6592-4a62-a96f-0f2b029f1478"
)

# Получаем данные о транзакциях
transactions = OzonTransaction.get_transactions(
    api=api,
    start_date=datetime.now() - timedelta(days=29),
    end_date=datetime.now()
)

filtered_list = [tr for tr in transactions if tr.order_type == 0]

print(filtered_list)

print(f"Всего операций: {len(filtered_list)}")
articles = []
[articles.append(tr.marketplace_product) for tr in filtered_list if tr.marketplace_product not in articles]
print(f"Всего артикулов: {len(articles)}")
print("Выбор артикула: sticks_steel_black")
product = next(OzonProduct.get_products_by_codes(api, ["sticks_steel_black"]))
print(f"Выбран id: {product.id}")
print(f"Склады: {[tr.warehouse_id for tr in filtered_list if tr.marketplace_product == 395571012]}")
product_transactions = [tr for tr in filtered_list if (tr.marketplace_product == 395571012)] #and tr.warehouse_id == None

print(f"Всего операций по артикулу: {len(product_transactions)}")

# Всего продано
total_sold = sum([int(tr.quantity-tr.refund) for tr in product_transactions])
print(f"Всего продано: {total_sold}")
# Среднее количество продаж в день
avg_count_per_day = total_sold / 30
print(f"Среднее количество продаж в день: {avg_count_per_day}")

# Среднеквадратичное отклонение расхода запаса
rms_deviation = 1.0
# math.sqrt(1/)

# Предиктовый рачет
predication = get_basic_predication_supplies_fos(size_supply=10,
                                                 avg_delivery_time=timedelta(days=3),  # Матрицы доставки
                                                 deviation_sales=rms_deviation,
                                                 avg_consumption=avg_count_per_day,
                                                 deviation_delivery_time=1)

print(f"Предиктивный расчет: {predication}")


# Даты между поставками
days = (predication.max_stock - predication.order_point) / avg_count_per_day
print(f"Даты между поставками: {days}")

print(f"Предполагаемая дата поставки: {datetime.now() + timedelta(days=days)}")

# Предиктовый рачет c фиксированным периодом поставки
print("---------------------------------------------------")
print("Предиктовый рачет c фиксированным периодом поставки")

avg_delivery_time = timedelta(days=3)
print(f"Время выполнения заказа: {avg_delivery_time.days}")

size_supply = 10
print(f"Оптимальная партия поставки: {size_supply}")

period = timedelta(days=15)
print(f"Длительность периода: {period}")

print(f"Средняя интенсивность потребления: {avg_count_per_day}")

rms_deviation = 6.0
print(f"Срасхода: {rms_deviation}")

predication = get_basic_predication_supplies_fof(size_supply=size_supply,
                                                 avg_consumption_per_day=avg_count_per_day,
                                                 avg_delivery_time=avg_delivery_time,  # Матрицы доставки
                                                 deviation_sales=rms_deviation,        # Среднеквадратичное отклонение расхода запаса
                                                 period=period,            # Период
                                                 consumption=total_sold,
                                                 current_stock=5
                                                 )

print(f"Предиктивный расчет c фиксированным периодом поставки: {predication}")

print(f"Предполагаемая дата поставки: {datetime.now() + predication.order_date}")


