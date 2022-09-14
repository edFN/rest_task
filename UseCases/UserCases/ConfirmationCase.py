from data.StorageUser import get_db_storage
from data.StorageBill import get_bill_db_storage
from sanic import Sanic
from sanic.response import json
from sanic import Request

from main import _config

from models.Bill import Bill

app = Sanic.get_app("App")

import jwt
ACCESS_TOKEN_SECRET = _config["TOKEN_SECRET"]

class ConfirmationCase:
    @app.post("/confirm/<token>")
    async def confirm(self, token):
        data = jwt.decode(token, ACCESS_TOKEN_SECRET, "HS256")

        usr = await get_db_storage().getUserByName(data.get("username"))

        if usr is None:
            return json({"err": 1})

        if usr.is_active: return json({"err": 1, "msg": "User is already verif"})

        usr.is_active = True

        res = await get_db_storage().update(usr)

        if res:
            bill = await get_bill_db_storage().insert(Bill(bill_id=0,owner_id=usr.user_id,balance=0))
            if bill:
                return json({"success": 1})
            else:
                return json({"error":1,"msg":"cannot be created"})
        else:
            return json({"err": 1, "msg": "User cant be activated"})