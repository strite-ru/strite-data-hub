import logging
from strite_data_hub.parsers.ozon.api import OzonAPI
from datetime import datetime, timedelta
from strite_data_hub.parsers.ozon.orders import OzonFBOPosting, OzonFBSPosting, OzonPosting
import pickle

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.ERROR
)
logger = logging.getLogger(__name__)

def init_data() -> OzonAPI:
    client_id = input("Client-Id: ", )
    api_key = input("Api-Key: ")

    return OzonAPI(client_id=int(client_id), key=api_key)


def main(days=350):
    api = init_data()

    postings_fbo = list(OzonFBOPosting.get_postings(api, status="delivered", date_from=(datetime.now() - timedelta(days=days))))
    postings_fbs = list(OzonFBSPosting.get_postings(api, status="delivered", date_from=(datetime.now() - timedelta(days=days))))

    print(f"Всего отправлений FBO: {len(postings_fbo)}")
    print(f"Всего отправлений FBS: {len(postings_fbs)}")

    # get parent orders
    all_postings: list[OzonPosting] = []
    for posting in postings_fbo:
        all_postings.append(
            OzonPosting(
                orderId=posting.orderId,
                postingNumber=posting.postingNumber,
                status=posting.status,
                orders=posting.orders,
                processTo=posting.processTo
            )
        )
    for posting in postings_fbs:
        all_postings.append(
            OzonPosting(
                orderId=posting.orderId,
                postingNumber=posting.postingNumber,
                status=posting.status,
                orders=posting.orders,
                processTo=posting.processTo
            )
        )

    print(f"Всего отправлений: {len(all_postings)}")

    with open('all_postings.pickle', 'wb') as f:
        pickle.dump(all_postings, f)

    print("Сохранено в all_postings.pickle")


if __name__ == '__main__':
    main()
