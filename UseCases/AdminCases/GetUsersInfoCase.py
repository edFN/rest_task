from decimal import Decimal

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from models.User import User

from data.StorageUser import get_db_storage

from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")


class GetUsersInfoCase:
    @app.get("/get_users")
    async def get_users_info(request:Request):
        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})

        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err": 1, "msg": "You dont' have permission"})

        users_info = await get_db_storage().get_all_users()

        users_info = {i: users_info[i].__dict__ for i in range(0, len(users_info))}

        return json({"success":1,"users": users_info})

