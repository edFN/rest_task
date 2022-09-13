
from decimal import Decimal

class Bill:
    bill_id: int
    balance: int
    owner_id: int

    def __init__(self,bill_id,balance,owner_id):
        self.bill_id = bill_id
        self.balance = balance.__int__()
        self.owner_id = owner_id