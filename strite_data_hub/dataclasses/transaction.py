from datetime import datetime
from decimal import Decimal
from dataclasses import dataclass
from typing import Self, Optional


@dataclass()
class TransactionData:
    transaction_id: Optional[int] = None
    transaction_type: Optional[int] = None
    transaction_date: Optional[datetime] = None
    order_id: Optional[int] = None
    order_type: Optional[int] = None
    order_date: Optional[datetime] = None
    marketplace_product: Optional[int] = None
    commission: Decimal = 0
    delivery: Decimal = 0
    quantity: int = 0
    refund: int = 0
    amount: Decimal = 0

    @property
    def pay(self) -> Decimal:
        return self.amount + self.commission + self.delivery

    def __eq__(self, another: Self):
        """Определение принадлежности к одному товару"""
        return self.marketplace_product == another.marketplace_product

    def __add__(self, another: Self):
        return TransactionData(
            commission=self.commission + another.commission,
            delivery=self.delivery + another.delivery,
            quantity=self.quantity + another.quantity,
            refund=self.refund + another.refund,
            amount=self.amount + another.amount,
            marketplace_product=self.marketplace_product if self == another else None
        )

    def __sub__(self, another: Self):
        return TransactionData(
            commission=self.commission - another.commission,
            delivery=self.delivery - another.delivery,
            quantity=self.quantity - another.quantity,
            refund=self.refund - another.refund,
            amount=self.amount - another.amount,
            marketplace_product=self.marketplace_product if self == another else None
        )
