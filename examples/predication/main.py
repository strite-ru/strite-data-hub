"""
Пример использования предикативного анализа

"""
import math
import logging
from strite_data_hub.parsers.ozon.api import OzonAPI
from strite_data_hub.prediction.supplies.basic.main import get_basic_predication_supplies_fos
from datetime import datetime, timedelta
from strite_data_hub.parsers.ozon.finance import OzonTransaction
from strite_data_hub.parsers.ozon.products import OzonProduct
from strite_data_hub.parsers.ozon.warehouses import OzonWarehouse, OzonStockOnWarehouse
from strite_data_hub.parsers.ozon.orders import OzonPosting
from rich.console import Console
from rich.live import Live
from rich.table import Table


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)


def calc(api: OzonAPI, period_transactions: int = 29):
    # Конфигурация вывода данных
    console = Console(safe_box=False, force_terminal=True)
    console.size = (250, 38)
    table = Table(show_footer=False)
    table.title = "Артикулы магазина"
    table.add_column("Артикул", no_wrap=True)
    table.add_column("Склад", no_wrap=True)
    table.add_column("Остаток", justify="center")
    table.add_column("Всего продано", justify="center")
    table.add_column("Среднее число продаж в день", justify="center")
    table.add_column("Среднеквадратичное отклонение", justify="center")
    table.add_column("FOS\nДней до поставки", justify="center")
    table.add_column("FOS\nПредполагаемая дата поставки", justify="center")

    # Получаем данные о транзакциях
    transactions = list(OzonTransaction.get_transactions(
        api=api,
        start_date=datetime.now() - timedelta(days=period_transactions),
        end_date=datetime.now()
    ))
    logger.info(f"Всего транзакций за период: {len(transactions)}")
    # Фильтруем операции по FBO
    fbo_transactions = [tr for tr in transactions if tr.order_type == 0]
    logger.info(f"Все операций по FBO: {len(fbo_transactions)}")

    # Список артикулов за период
    skus = list({tr.marketplace_product for tr in fbo_transactions})
    logger.info(f"Всего sku за период: {len(skus)}")

    # Список складов
    warehouses = list(OzonWarehouse.get_warehouses(api))
    stocks = list(OzonStockOnWarehouse.get_stocks(api))

    products = list(OzonProduct.get_products(api))

    if len(products) == 0:
        logger.warning("нет информации об товарах")
        return

    with Live(table, console=console, screen=False):
        for sku in skus:
            def get_product() -> OzonProduct | None:
                _p = None
                for item in products:
                    if next((item for _size in item.sizes if _size.id == sku and _size.type == 'fbo'), None):
                        _p = item
                return _p

            product: OzonProduct | None = get_product()

            if product is None:
                logger.info(f"Мы пропускаем sku {sku}. Нет информации о товаре")
                continue

            # Транзакции по товару
            product_transactions = [tr for tr in fbo_transactions if (tr.marketplace_product == sku)]
            # Отправления по товару
            product_postings = list({tr.order_id for tr in product_transactions})
            product_warehouses = {}
            for p_n in product_postings:
                posting = OzonPosting.get_fbo_posting_by_posting_number(api, p_n)
                count = sum([o.quantity for o in posting.orders if o.vendor_code == product.vendor_code], 0)
                if product_warehouses.get(posting.warehouse_id, None):
                    product_warehouses[posting.warehouse_id] += count
                else:
                    product_warehouses[posting.warehouse_id] = count

            table.add_row(product.vendor_code)

            for warehouse_id in product_warehouses.keys():
                warehouse = [w for w in warehouses if w.id == str(warehouse_id)][0]

                total_sold = product_warehouses[warehouse_id]
                avg_count_per_day = total_sold / period_transactions

                # TODO add calc
                rms_deviation = 1.0

                # Среднее время доставки (из матрицы доставки) + обработки
                avg_delivery_time = timedelta(days=3)

                predication = get_basic_predication_supplies_fos(size_supply=10,
                                                                 avg_delivery_time=avg_delivery_time,
                                                                 deviation_sales=rms_deviation,
                                                                 avg_consumption=avg_count_per_day,
                                                                 deviation_delivery_time=1)

                # Текущий остаток на складе
                stock_search = [s for s in stocks if s.vendor_code == product.vendor_code and s.warehouse == warehouse]
                if len(stock_search) == 0:
                    logger.warning(f"Нет стока для {product.vendor_code}, склад: {warehouse.name}")
                    stock = 0
                else:
                    stock = stock_search[0].free_to_sell_amount

                # Даты между поставками
                days = (stock - predication.order_point) / avg_count_per_day

                table.add_row(
                    "",
                    warehouse.name,
                    str(stock),
                    str(total_sold),
                    "{:.2f}".format(avg_count_per_day),
                    str(rms_deviation),
                    str(int(days)),
                    (datetime.now() + timedelta(days=days)).strftime("%d.%m.%Y")
                )


if __name__ == '__main__':
    api = OzonAPI(
        client_id=0,
        key="xxxx"
    )

    calc(api)
