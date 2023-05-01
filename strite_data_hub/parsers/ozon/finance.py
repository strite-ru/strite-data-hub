from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

from strite_data_hub.dataclasses import TransactionData
from ..utils import get_transaction_type
from .api import OzonAPI
import logging

logger = logging.getLogger("Strite")


@dataclass()
class OzonTransaction(TransactionData):

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        tr_type = get_transaction_type(raw_data['operation_type'])

        return cls(
            transaction_id=raw_data['operation_id'],
            transaction_type=tr_type,
            transaction_date=datetime.strptime(raw_data['operation_date'], "%Y-%m-%d %X"),
            order_id=raw_data['posting']['posting_number'],
            order_type=0 if raw_data['posting']['delivery_schema'] == 'FBO' else 1,
            order_date=datetime.strptime(raw_data['posting']['order_date'], "%Y-%m-%d %X"),
            commission=raw_data.get('amount', 0) if tr_type == 3 else raw_data.get('sale_commission', 0),
            delivery=sum(service['price'] for service in raw_data.get('services', [])),
            quantity=len(raw_data['items']) if tr_type == 0 else 0,
            refund=len(raw_data['items']) if tr_type == 2 else 0,
            amount=raw_data.get('accruals_for_sale', 0),
            marketplace_product=raw_data['product_id'] if 'product_id' in raw_data else 0
        )

    @classmethod
    def get_transactions(cls,
                         api: OzonAPI,
                         start_date: datetime = datetime.now() - timedelta(days=30),
                         end_date: datetime = datetime.now()) -> list[Self]:
        body = {
            "filter": {
                "date": {
                    "from": start_date.strftime("%Y-%m-%dT00:00:00.000Z"),
                    "to": end_date.strftime("%Y-%m-%dT23:59:59.999Z")
                },
                "operation_type": [
                    "OperationAgentDeliveredToCustomer",
                    "OperationItemReturn",
                    "ClientReturnAgentOperation",
                    "OperationReturnGoodsFBSofRMS",
                    "OperationMarketplaceServicePremiumCashback"
                ],
                "transaction_type": "all"
            },
            "page": 1,
            "page_size": 100000
        }

        while True:
            raw_data = api.request(url="v3/finance/transaction/list",
                                   method="POST",
                                   body=body)

            if not raw_data.get('result', False):
                logger.error(msg := "Не смогли получить транзакции магазина Ozon")
                raise Exception(msg)

            pre_processing_data = []

            #  pre-processing
            for operation in raw_data['result']['operations']:
                _orders = []

                for item in operation['items']:
                    _orders.append(item['sku'])

                if len(list(set(_orders))) == 1:
                    operation['product_id'] = _orders[0]
                    pre_processing_data.append(operation)
                else:
                    if operation['posting']['delivery_schema'] == "FBO":
                        body_posting = {
                            "posting_number": operation['posting']['posting_number'],
                            "translit": True,
                            "with": {
                                "analytics_data": False,
                                "financial_data": True
                            }
                        }
                        raw_posting = api.request(url="v2/posting/fbo/get",
                                                  method="POST",
                                                  body=body_posting)
                    else:
                        body_posting = {
                            "posting_number": operation['posting']['posting_number'],
                            "translit": True,
                            "with": {
                                "analytics_data": False,
                                "barcodes": False,
                                "financial_data": True,
                                "translit": False
                            }
                        }
                        raw_posting = api.request(url="v2/posting/fbs/get",
                                                  method="POST",
                                                  body=body_posting)

                    if not raw_posting.get('result', False):
                        logger.error(msg := "Не смогли получить постинг магазина Ozon")
                        raise Exception(msg)

                    order = raw_posting['result']

                    for idx, product in enumerate(raw_posting['result']['products']):
                        # sham operation
                        pre_processing_data.append({
                            'operation_id': operation['operation_id'],
                            'operation_type': operation['operation_type'],
                            'operation_date': operation['operation_date'],
                            'posting': {
                                'delivery_schema': operation['posting']['delivery_schema'],
                                'order_date': operation['posting']['order_date'],
                                'posting_number': operation['posting']['posting_number']
                            },
                            'services': [
                                {'price': sum(service['price'] for service in operation['services']) / len(
                                    operation['items']) * product['quantity']}
                            ],
                            'product_id': product['sku'],
                            'sale_commission': 0 - order['financial_data']['products'][idx]['commission_amount'],
                            'accruals_for_sale': order['financial_data']['products'][idx]['price'],
                            'items': [{} for _ in range(product['quantity'])]
                        })

            #  parse
            yield from (cls.parse_from_dict(p_data) for p_data in pre_processing_data)

            if raw_data['result']['row_count'] != body['page_size']:
                break
            else:
                body['page'] += 1
