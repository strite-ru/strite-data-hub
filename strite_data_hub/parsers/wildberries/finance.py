from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Self

from ..general_datastrutures import TransactionData
from ..utils import get_transaction_type
from .api import WildberriesAPI
import logging

logger = logging.getLogger("Strite")


@dataclass()
class WbTransaction(TransactionData):

    @classmethod
    def parse_from_dict(cls, raw_data: dict) -> Self:
        tr_type = get_transaction_type(raw_data['supplier_oper_name'])

        amount = 0
        commission = 0
        quantity = 0
        refund = 0
        if tr_type in [0, 1]:
            amount = raw_data['retail_amount']
            commission -= raw_data['retail_amount'] - raw_data['ppvz_for_pay']
            quantity = raw_data['quantity']
            refund = raw_data['return_amount']
        elif tr_type == 2:
            amount -= raw_data['retail_amount']
            commission = raw_data['retail_amount'] - raw_data['ppvz_for_pay']
            refund = raw_data['quantity']

        return cls(
            transaction_id=raw_data['rrd_id'],
            transaction_type=tr_type,
            transaction_date=datetime.strptime(raw_data['rr_dt'], "%Y-%m-%dT%XZ"),
            order_id=raw_data['rid'],
            order_type=0 if raw_data['office_name'] else 1,
            order_date=datetime.strptime(raw_data['order_dt', "%Y-%m-%dT%XZ"]),
            commission=commission,
            delivery=raw_data['delivery_rub'],
            amount=amount,
            quantity=quantity,
            refund=refund,
            marketplace_product=raw_data['nm_id']
        )

    @classmethod
    def get_transactions(cls,
                         api: WildberriesAPI,
                         start_date: datetime = datetime.now() - timedelta(days=30),
                         end_date: datetime = datetime.now()) -> list[Self]:
        params = {
            "dateFrom": start_date.strftime('%Y-%m-%d'),
            "dateTo": end_date.strftime('%Y-%m-%d'),
            "rrdId": 0,
            "limit": 1000,
        }
        while True:
            raw_data = api.statistics_request(url="https://statistics-api.wildberries.ru/api/v1/supplier/reportDetailByPeriod",
                                              params=params)

            yield from (cls.parse_from_dict(p_data) for p_data in raw_data)

            if len(raw_data) < params['limit']:
                break
            else:
                params['rrdid'] = raw_data[-1]['rrd_id']
