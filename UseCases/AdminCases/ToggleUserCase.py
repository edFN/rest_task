from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from data.StorageUser import get_db_storage

from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")


class ToggleUserCase:
    @app.post("/toggle_user/<user_id>")
    async def toggle_user(request:Request,user_id:int):

        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})


        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err": 1, "msg": "You dont' have permission"})

        user_to_toggle = await get_db_storage().getUser(user_id)

        user_to_toggle.is_active = not user_to_toggle.is_active

        res = await get_db_storage().update(user_to_toggle)

        if res:
            return json({"success":1,"msg":"switched"})
        else:
            return json({"err":1,"msg":"not switched"})

