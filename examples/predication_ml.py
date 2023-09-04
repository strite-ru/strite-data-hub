import logging
from datetime import datetime, timedelta
from typing import List

from strite_data_hub.parsers.ozon import OzonAPI, OzonFBOPosting, OzonWarehouse
from strite_data_hub.parsers.ozon.utils import get_clusters_with_warehouses
from strite_data_hub.prediction.supplies.catboost import get_prediction

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.captureWarnings(True)
logger = logging.getLogger(__name__)


def init_data() -> OzonAPI:
    client_id = input("Client-Id: ", )
    api_key = input("Api-Key: ")

    return OzonAPI(client_id=int(client_id), key=api_key)


def main():
    api = init_data()

    clusters = get_clusters_with_warehouses()

    postings: List[OzonFBOPosting] = list(OzonFBOPosting.get_postings(api,
                                                                      status="delivered",
                                                                      date_from=(datetime.now() - timedelta(days=180))))

    logger.info(f"Всего отправлений: {len(postings)}")
    print(f"Всего отправлений: {len(postings)}")

    def merge_data_by_week_and_product():
        """Объединение данных о продажах по неделям, артикулам и кластерам"""
        result = []
        for posting in postings:
            for o_product in posting.orders:
                cluster = next((c for c in clusters if str(posting.warehouse['id']) in [w.id for w in c.warehouses]), None)
                if cluster:
                    cluster_name = cluster.name
                else:
                    cluster_name = 'None'
                product = next((p for p in result if p['week'] == posting.processTo.isocalendar()[1] and p['vendor_code'] == o_product.vendor_code and p['cluster'] == cluster_name), None)


                if product is None:
                    result.append({
                        'week': posting.processTo.isocalendar()[1],
                        'vendor_code': o_product.vendor_code,
                        'log_sales_total': o_product.quantity,
                        'avg_price': o_product.price,
                        'cluster': cluster_name
                    })
                else:
                    product['log_sales_total'] += o_product.quantity
                    product['avg_price'] += o_product.price

        for r in result:
            r['avg_price'] /= r['log_sales_total']
        return result

    data = merge_data_by_week_and_product()
    print(f"Всего продаж: {len(data)}")

    predicts = []
    for product in data:
        if product['vendor_code'] not in [p['vendor_code'] for p in predicts]:
            predicts.append({
                'vendor_code': product['vendor_code'],
                'week': (datetime.now()+timedelta(weeks=1)).isocalendar()[1],
                'avg_price': product['avg_price'],
            })
    print(f"Всего предсказаний: {len(predicts)}")
    results = get_prediction(data, predicts)
    print(f"Всего результатов: {len(results)}")
    print("----------------")
    for idx, value in enumerate(results):
        predict = predicts[idx]
        product_data = [d for d in data if d['vendor_code'] == predict['vendor_code']]
        last_week = max([d['week'] for d in product_data])
        last_data = [d for d in product_data if d['week'] == last_week][0]
        print(f"Vendor code: {predict['vendor_code']}")
        print(f"Predict week: {predict['week']}")
        print(f"Price: {predict['avg_price']}")
        print(f"Last week: {last_data['log_sales_total']}")
        print(f"Predict sales: {round(value, 2)} ({round(value / last_data['log_sales_total'] * 100 - 100, 2)}%)")
        print("----------------")







if __name__ == '__main__':
    main()