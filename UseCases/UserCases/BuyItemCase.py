


#buy_product(product_id, user_id)
#1.0 check header for auth
    #1.1 if not auth send message you need to login
    #1.2.else get user money
#2.0 check if exist product with product_id
    #2.1 if so check his price
    #2.2 send message that it doesnt exists
#3.0 get_all_bills_of user
    #3.1 check what bill can be affected
import jwt
from sanic import Sanic
from sanic.request import Request
from sanic.response import json
from utils.auth_tools import decode_token
from data.StorageBill import get_bill_db_storage
from data.StorageProduct import get_product_db_storage

from models.Bill import  Bill

app = Sanic.get_app("App")

#awaites!!!

#need to test!!!!

class BuyItemCase:
    @app.post("/buy_product/<product_id>")
    async def buy_product(request: Request, product_id):

        if request.headers["Authorization"] is None:
            return json({"err":1,"msg":"need to auth"})

        authorization_split = request.headers["Authorization"].split()
        bearer = authorization_split[0]
        if bearer != "Bearer": return json({"err":1,"msg":"need to auth"})

        token = authorization_split[1]

        token_data = decode_token(token)

        if token_data is None:
            return json({"err": 1, "msg": "may be wrong token"})

        user_id = token_data['user_id']

        product = await get_product_db_storage().get_product(product_id)

        if product is None:
            return json({"err": 1, "msg": "product with this id not ava"})

        first_bill = await get_bill_db_storage().get_user_bill_enough(user_id,product.price)

        if first_bill is None:
            return json({"err":1,"msg":"not enough money"})

        first_bill.balance -= product.price

        await get_bill_db_storage().update(first_bill)

        #add bill substraction
        return json({"success":1,"msg": "OK"})








