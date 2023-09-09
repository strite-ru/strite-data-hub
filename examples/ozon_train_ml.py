import logging
import os.path

from rich.console import Console
from rich.table import Table
import pickle

from strite_data_hub.prediction.supplies.catboost import train_model_by_ozon_postings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)


def main():
    # Как получить все товары и отправления с ozon см. в examples/ozon_get_all_posting.py и examples/ozon_get_product.py
    with open('all_products.pickle', 'rb') as f:
        products = pickle.load(f)

    with open('all_postings.pickle', 'rb') as f:
        postings = pickle.load(f)

    print(f"Всего отправлений: {len(postings)}")
    print(f"Всего товаров: {len(products)}")

    model, test_predicts = train_model_by_ozon_postings(products, postings)

    console = Console()

    table = Table(title="Предсказание продаж на 7 дней")
    table.add_column("Артикул", justify="left", style="cyan", no_wrap=True)
    table.add_column("Предсказание", justify="center", style="cyan", no_wrap=True)
    table.add_column("Фактически", justify="center", style="cyan", no_wrap=True)

    for row in test_predicts:
        table.add_row(
            row['vendor_code'],
            str(round(row['predict'])),
            str(row['actual'])
        )

    console.print(table)


if __name__ == '__main__':
    main()
