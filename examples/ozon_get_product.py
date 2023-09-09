import logging
import pickle

from strite_data_hub.parsers.ozon.api import OzonAPI
from strite_data_hub.parsers.ozon.products import OzonProduct

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)

def init_data() -> OzonAPI:
    client_id = input("Client-Id: ", )
    api_key = input("Api-Key: ")

    return OzonAPI(client_id=int(client_id), key=api_key)


def main():
    api = init_data()

    products = list(OzonProduct.get_products(api))

    with open('all_products.pickle', 'wb') as f:
        pickle.dump(products, f)

    print(products)


if __name__ == '__main__':
    main()
