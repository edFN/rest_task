from abc import abstractmethod
from models.User import User
from utils import database
from typing import Union


class UserStorage:
    @abstractmethod
    async def insert(self, user: User) -> bool:
        pass
    @abstractmethod
    async def update(self,user: User) -> bool:
        pass

    @abstractmethod
    async def getUser(self, user_id: int) -> Union[User,None]:
        pass

    @abstractmethod
    async def getUserByName(self,username: str) -> Union[User,None]:
        pass

    @abstractmethod
    async def get_all_users(self) -> Union[list,None]:
        pass


class UserDatabaseStorage(UserStorage):

    def __init__(self):
        self.query = database.query

    async def insert(self,user: User)->bool:
        return self.query.insert("User",{
            "username": "\'" + user.username + "\'",
            "password_hash": "\'" + user.password_hash + "\'"
        })

    async def update(self, user: User)->bool:

        where = f"user_id = {user.user_id}"

        params = {
            "username" : "\'"+user.username + "\'",
            "password_hash" : "\'"+user.password_hash + "\'",
            "is_active": user.is_active
        }
        res = await self.query.update("User", where, params)

        return res

    async def getUser(self, user_id: int) -> Union[User,None]:
        response =  await self.query.select("User",f"user_id = {user_id}")

        if response is None:
            return None

        return User(response[0], response[2], response[1], response[3], response[4])

    async def getUserByName(self, username: str) -> Union[User,None]:

        response = await self.query.select("User", f"username = \'{username}\'")

        if response is None:
            return None

        return User(response[0], response[2], response[1], response[3], response[4])

    async def get_all_users(self) -> Union[list,None]:
        response = await self.query.selectAll("User")

        if response is None: return None

        users = [User(item[0],item[2],item[1],item[3],item[4]) for item in response]

        return users

def get_db_storage() -> UserDatabaseStorage:
    return UserDatabaseStorage()








