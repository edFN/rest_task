import datetime


class Transaction:
    transaction_id: int
    time: datetime.datetime
    amount: int
    bill_id: int

    def __init__(self,transaction_id:int,time:datetime.datetime,amount:int,bill_id:int):
        self.transaction_id = transaction_id
        self.time = time
        self.amount = amount
        self.bill_id = bill_id
