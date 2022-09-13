
from sanic import Sanic
from sanic.request import Request
from sanic.response import json

import models.Product
from data.StorageProduct import get_product_db_storage
from models import Product

from json import dumps


app = Sanic.get_app("App")

class GetProductCase:
    @app.get("/products")
    async def get_products(request: Request):

        storage = get_product_db_storage()

        products = await storage.get_products()

        if products is None:
            return json({"err": 1, "message": "empty"})

        products = {i : products[i].__dict__ for i in range(0,len(products))}
        return json({"success": 1,"product_list": products})







