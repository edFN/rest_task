from abc import abstractmethod
from utils.database import query
from models.Bill import  Bill
from typing import Union
from decimal import Decimal

class StorageBill:
    @abstractmethod
    async def get_user_bills(self,user_id) -> Union[list,None]:
        pass
    @abstractmethod
    async def get_user_bill_enough(self,user_id, product_price)->Union[Bill,None] :
        pass

    @abstractmethod
    async def get_bill_id(self,bill_id)->Union[Bill,None]:
        pass

    @abstractmethod
    async def update(self,bill: Bill)->bool:
        pass

class BillDatabaseStorage(StorageBill):



    def __init__(self):
        self.query = query

    async def get_bill_id(self, bill_id) -> Union[Bill,None]:
        bill = await self.query.select("Bill",f"bill_id = {bill_id}")
        if bill is None: return None

        return Bill(bill[0],bill[1],bill[2])


    async def get_user_bill_enough(self, user_id, product_price) -> Union[Bill,None]:
        bill = await self.query.select("Bill",f"owner_id = {user_id} AND balance >= {product_price}")

        if bill is None: return None

        return Bill(bill[0],bill[1],bill[2])

    async def get_user_bills(self, user_id)->Union[list,None]:
        rows = await self.query.selectAll("Bill",f"owner_id = {user_id}")

        if rows is None:
            return None

        bills = [Bill(row[0],row[1],row[2]) for row in rows]

        return bills

    async def update(self,bill: Bill) ->bool:
        is_ok = await self.query.update("Bill",f"bill_id = {bill.bill_id}", {
            "balance": Decimal(bill.balance)
        })
        return is_ok
def get_bill_db_storage() -> BillDatabaseStorage:
    return BillDatabaseStorage()



