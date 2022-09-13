from typing import Any
from sanic.request import Request
from Crypto.Hash import SHA256
from datetime import datetime, timedelta
import jwt


from typing import Union
from main import _config

from models.User import User

TOKEN_SECRET = _config["TOKEN_SECRET"]

def hash_password(password: str):
    hash = SHA256.new()
    hash.update(bytes(password,"UTF-8"))
    return hash.hexdigest()

def generate_token(params: dict):

    payloads = {
        "exp": datetime.utcnow() + timedelta(minutes=10)
    }
    payloads.update(params)

    encode_jwt = jwt.encode(payload=payloads, algorithm="HS256", key=TOKEN_SECRET)
    return encode_jwt

def decode_token(token) -> Union[None,dict]:
    try:
        res = jwt.decode(token,algorithms="HS256",key=TOKEN_SECRET)
        return res
    except jwt.InvalidTokenError:
        return None


def check_authorization(request:Request) -> Union[None,dict]:
    if request.headers.get("Authorization") is None:
        return None

    authorization_split = request.headers["Authorization"].split()
    bearer = authorization_split[0]

    if bearer != "Bearer":
        return None

    token = request.headers["Authorization"].split()[1]

    token_data = decode_token(token)

    if token_data is None: return None

    return token_data




