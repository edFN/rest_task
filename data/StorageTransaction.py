from abc import abstractmethod
from decimal import Decimal

from models.Transaction import Transaction
from utils.database import query


class StorageTransaction:
    @abstractmethod
    async def add(self,transaction: Transaction)->bool:
        pass


class StorageDatabaseTransaction(StorageTransaction):

    def __init__(self):
        self.query = query

    async def add(self, transaction: Transaction)->bool:
        res = await query.insert("Transaction",params={
            "transaction_id": transaction.transaction_id.__str__(),
            "time": "\'" +transaction.time.__str__()+ "\'",
            "amount": transaction.amount.__str__(),
            "bill_id": transaction.bill_id.__str__()
        })
        return res

def get_trasaction_db_storage()->StorageDatabaseTransaction:
    return StorageDatabaseTransaction()