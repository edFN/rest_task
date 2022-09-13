from datetime import datetime, timedelta

from sanic import Sanic
from sanic.response import json
from sanic import Request


from data.StorageUser import get_db_storage
from utils.auth_tools import hash_password,generate_token

from models.User import User

ACCESS_TOKEN_SECRET = "my_secret_token"

app = Sanic.get_app("App")


class RegisterCase:
    @app.post("/register")
    async def register(request: Request):

        username = request.get_form().get("username")

        if username is None:
            raise ValueError

        password = request.get_form().get("password")

        if password is None: raise ValueError

        usr = await get_db_storage().getUserByName(username)

        if usr is not None: return json({"err": "1"})

        password_hash = hash_password(password)
        usr = User(username,password_hash)

        res = await get_db_storage().insert(usr)

        if res:
            encode_jwt = generate_token({
                "user": username
            })
            return json({"success": 1, "url_confirm": "http://localhost:8000/confirm/" + encode_jwt})

        else:
            return json({"msg": "bad"})
