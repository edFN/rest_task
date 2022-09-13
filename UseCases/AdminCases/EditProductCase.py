
from sanic import Sanic
from sanic.request import Request
from sanic.response import json

from models.Product import Product

from data.StorageProduct import get_product_db_storage
from data.StorageUser import get_db_storage

from utils.auth_tools import decode_token,check_authorization

app = Sanic.get_app("App")

class EditProductCase:
    @app.post("/edit/<product_id>")
    async def edit_product(request:Request,product_id:int):

        token_data = check_authorization(request)

        if token_data is None:
            return json({"err": 1, "msg": "need to auth"})

        title = request.get_form().get("title")
        description = request.get_form().get("description")
        price = request.get_form().get("price")


        usr = await get_db_storage().getUser(token_data["user_id"])

        if not usr.is_admin:
            return json({"err": 1, "msg": "You dont' have permission"})

        product = await get_product_db_storage().get_product(product_id)

        if product is None:
            return json({"err":1,"msg":"couldnt find"})

        if price is not None: product.price = price
        if description is not None: product.description = description
        if title is not None: product.title = title

        res = await get_product_db_storage().edit(product)

        if res:
            return json({"success":1,"msg":"updated"})
        else:
            return json({"err":1,"msg":"not updated"})


