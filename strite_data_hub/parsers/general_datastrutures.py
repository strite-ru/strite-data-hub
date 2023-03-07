from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass


@dataclass()
class TransactionData:
    transaction_id: int
    transaction_type: int
    transaction_date: datetime
    order_id: int
    order_type: int
    order_date: datetime
    marketplace_product: int = 0
    commission: Decimal = 0
    delivery: Decimal = 0
    quantity: int = 0
    refund: int = 0
    amount: Decimal = 0

    @property
    def pay(self) -> Decimal:
        return self.amount + self.commission + self.delivery
