from sanic import Sanic
import json


app = Sanic("App")

file = open("config.json","r")
if file.closed:
    print("Cannot read config.json")
    exit(1)

_config = json.load(file)

file.close()

from UseCases.UserCases import BuyItemCase,ConfirmationCase,GetBillsCase,\
    GetProductCase,LoginCase,RegisterCase
from UseCases.AdminCases import CreateProductCase,DeleteProductCase,ToggleUserCase,GetUsersInfoCase,EditProductCase
from UseCases.Webhooks import TransactionWebHook




