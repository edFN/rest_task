from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from models.Product import Product

from data.StorageProduct import get_product_db_storage
from data.StorageUser import get_db_storage

from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")

class DeleteProductCase:
    @app.post("/delete_product/<product_id>")
    async def delete_product(request:Request,product_id):

        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})

        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err": 1, "msg": "You dont' have permission"})

        res = await get_product_db_storage().delete(product_id)

        if res:
            return json({"success":1,"msg":"deleted"})
        else:
            return json({"err":1,"msg":"not deleted"})

