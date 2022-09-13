import psycopg2
from psycopg2.extras import wait_select
from typing import  Union
class Database:
    def __init__(self, dbname, host, port, user, password):

        try:

            self.con = psycopg2.connect(dbname=dbname, host=host, port=port,
                                        user=user,
                                        password=password,async_=1)
            #wait_select(conn=self.con)

            self.cursor = self.con.cursor()

        except psycopg2.Error as e:
            raise e

    def __init__(self,config: dict):

        try:
            self.con = psycopg2.connect(dbname=config.get("DB_NAME"), host=config.get("DB_HOST"), port=config.get("DB_PORT"),
                                        user=config.get("DB_USERNAME"),
                                        password = config.get("DB_PASSWORD"))

            self.cursor = self.con.cursor()
        except psycopg2.Error as e:
            print(e.pgerror)
            raise e


class Query:
    _database: Database

    def __init__(self, database: Database):
        self._database = database

    async def selectAll(self, table: str, whereBody="1=1") -> Union[list,None]:
        try:
            request = f"SELECT * FROM \"{table}\" WHERE({whereBody})"
            self._database.cursor.execute(request)
            return self._database.cursor.fetchall()
        except psycopg2.Error as e:
            return None


    async def selectById(self, table: str, key: str, id: str) -> Union[tuple,None]:
        try:
            request = f"SELECT * FROM \"{table}\" WHERE({key} = {id})"
            self._database.cursor.execute(request)
            return self._database.cursor.fetchone()
        except psycopg2.Error:
            return None

    async def select(self,table: str, whereBody: str) -> Union[tuple,None]:
        request = f"SELECT * FROM \"{table}\" WHERE( {whereBody})"
        self._database.cursor.execute(request)
        return self._database.cursor.fetchone()

    async def insert(self, table: str, params: dict) -> bool:

        request = f"INSERT INTO \"{table}\" ({','.join(params.keys())}) VALUES({','.join(params.values())})"
        try:
            self._database.cursor.execute(request)
            self._database.con.commit()
            return True
        except psycopg2.Error as e:
            print(e.pgerror)
            return False

    async def update(self,table: str,where: str ,params: dict) -> bool:
        update_param = []

        for k,v in params.items():
            update_param.append(f"{k} = {v}")
        request = f"UPDATE \"{table}\" SET {','.join(update_param)} WHERE({where})"
        try:
            self._database.cursor.execute(request)
            self._database.con.commit()
            return True
        except psycopg2.Error as e :
            return False
    async def delete(self,table:str,whereBody) -> bool:
        request = f"DELETE FROM \"{table}\" WHERE ({whereBody})"
        try:
            self._database.cursor.execute(request)
            self._database.con.commit()
            return True
        except psycopg2.Error as e:
            return False

from main import _config
print(_config)
data = Database(_config)

query = Query(data)