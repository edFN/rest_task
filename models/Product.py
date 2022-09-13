import json
from decimal import Decimal
from json import JSONEncoder
from typing import Any


class Product:
    product_id: int
    title: str
    description: str
    price : int

    def __init__(self,product_id,title,description,price: Decimal):
        self.product_id = product_id
        self.title = title
        self.description = description
        self.price = price.__int__()

    def create(title:str, description: str, price: Decimal):
        return Product(0,title,description,price)


