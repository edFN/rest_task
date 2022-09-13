from decimal import Decimal

from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from models.Product import Product

from data.StorageProduct import get_product_db_storage
from data.StorageUser import get_db_storage

from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")

class CreateProductCase:
    @app.post("/create_product")
    async def create_product(request: Request):

        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})


        title = request.get_form().get("title")

        if title is None: raise ValueError

        description = request.get_form().get("description")

        if description is None: raise  ValueError

        price = request.get_form().get("price")

        if price is None: raise ValueError

        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err":1,"msg":"You dont' have permission"})

        product = Product.create(title,description,Decimal(price))

        res = await get_product_db_storage().create(product)

        if res:
            return json({"success": 1,"msg": f"{title} create success"})
        else:
            return json({"err": 1, "msg":"cant create"})
