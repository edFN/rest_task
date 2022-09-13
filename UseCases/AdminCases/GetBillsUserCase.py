from decimal import Decimal

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from models.User import User
from models.Bill import Bill

from data.StorageUser import get_db_storage
from data.StorageBill import get_bill_db_storage
from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")


class GetBiilsUserCase:
    @app.get("/get_bills_user/<user_id>")
    def get_bills_user(request:Request,user_id):
        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})

        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err": 1, "msg": "You dont' have permission"})

        bills = await get_bill_db_storage().get_user_bills(user_id)

        bills = {i: bills[i].__dict__ for i in range(0,len(bills))}

        return json({
            "success":1,
            "bills": bills
        })
