


from sanic import Sanic
from sanic import Request

from sanic.response import json

from data.StorageUser import get_db_storage
from utils.auth_tools import hash_password,generate_token,check_authorization

app = Sanic.get_app("App")


class LoginCase:
    @app.post("/login")
    async def login(request: Request):

        if check_authorization(request) is not None:
            return json({"err": 1, "msg": "already logged in"})


        username = request.get_form().get("username")

        if username is None: raise ValueError

        password = request.get_form().get("password")

        if password is None: raise ValueError

        row = await get_db_storage().getUserByName(username)

        if row is None:
            return json({"err": 1})

        password_hash = hash_password(password)

        if row.password_hash == password_hash:
            jwt_token = generate_token({"user_id":row.user_id})
            return json({"token": jwt_token})

        return json({"err": 1})




