from data.StorageUser import get_db_storage
from sanic import Sanic
from sanic.response import json
from sanic import Request

app = Sanic.get_app("App")

import jwt
ACCESS_TOKEN_SECRET = "my_secret_token"

class ConfirmationCase:
    @app.post("/confirm/<token>")
    def confirm(self, token):
        data = jwt.decode(token, ACCESS_TOKEN_SECRET, "HS256")
        usr = get_db_storage().getUserByName(data.get("username"))

        if usr is None:
            return json({"err": 1})

        if usr.is_active: return json({"err": 1, "msg": "User is already verif"})

        usr.is_active = True

        res = get_db_storage().update(usr)

        if res:
            return json({"success": 1})
        else:
            return json({"err": 1, "msg": "User cant be activated"})