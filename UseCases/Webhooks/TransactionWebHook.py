import datetime

import asyncio

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from data.StorageBill import get_bill_db_storage
from data.StorageTransaction import  get_trasaction_db_storage
from models.Transaction import Transaction

app = Sanic.get_app("App")

class TransactionWebHook:
    @app.post("/payments/webhook")
    async def transaction_webhook(request: Request):

        signature = request.json["signature"]
        user_id = request.json["user_id"]
        bill_id = request.json["bill_id"]
        amount  = request.json["amount"]
        transaction_id = request.json["transaction_id"]

        if amount <= 0: raise ValueError

        bill = await get_bill_db_storage().get_bill_id(bill_id)

        if bill is None:
            return json({"err":1})

        bill.balance += amount

        transaction = Transaction(transaction_id,datetime.datetime.utcnow(),amount,bill_id)

        insert_complete = await get_trasaction_db_storage().add(transaction)

        if not insert_complete:
            return json("Error Transaction")

        update_complete = await get_bill_db_storage().update(bill)


        return json({"success":1})


