from abc import abstractmethod
from decimal import Decimal

from models.Product import Product
from utils.database import query
from typing import Union


class ProductStorage:

    @abstractmethod
    async def create(self,product:Product) -> bool:
        pass

    @abstractmethod
    async def edit(self,new_product: Product) ->bool:
        pass

    @abstractmethod
    async def delete(self,product_id)->bool:
        pass


    @abstractmethod
    async def get_products(self) -> Union[list, None]:
        pass
    @abstractmethod
    async def get_product(self) -> Union[Product, None]:
        pass


class ProductDatabaseStorage(ProductStorage):

    def __init__(self):
        self.query = query

    async def create(self, product: Product) -> bool:
        res = await self.query.insert("Product",params={
            "title": "\'"+product.title+"\'",
            "description": "\'"+product.description+"\'",
            "price": product.price.__str__()
        })
        return res

    async def edit(self, new_product: Product) -> bool:
        res = await self.query.update("Product",f"product_id = {new_product.product_id}",params={
            "title": "\'"+new_product.title+"\'",
            "description": "\'"+new_product.description+"\'",
            "price": new_product.price.__str__()
        })
        return res

    async def delete(self, product_id):
        res = await self.query.delete("Product",f"product_id = {product_id}")
        return res



    async def get_product(self, id) -> Union[Product, None]:

        data = await self.query.select("Product",f"product_id = {id}")

        if data is None: return None

        return Product(data[0],data[1],data[2],data[3])

    async def get_products(self) -> Union[list,None]:
        data = await self.query.selectAll("Product")

        if data is None: return None

        products = [Product(row[0],row[1],row[2],row[3]) for row in data]

        return products

def get_product_db_storage() -> ProductDatabaseStorage:
    return ProductDatabaseStorage()