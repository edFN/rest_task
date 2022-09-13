from sanic import Sanic
from sanic.response import json
from sanic.response import Request
from utils.auth_tools import decode_token,check_authorization

from data.StorageBill import get_bill_db_storage

app = Sanic.get_app("App")

class GetBillsCase:
    @app.get("/bills")
    async def get_bills(request: Request):

        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})

        if token_data is None: return json({"err": 1, "msg": "need to auth"})

        bills = await get_bill_db_storage().get_user_bills(token_data["user_id"])

        if len(bills) == 0:
            return json({"success": 1, "msg":"User dont have any bills"})

        bills = {i: bills[i].__dict__ for i in range(0, len(bills))}
        return json({"success":1,"bills": bills})


