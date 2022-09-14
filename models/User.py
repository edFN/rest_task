
class User:
    user_id: int
    username: str
    password_hash: str
    is_admin: bool
    is_active: bool



    def __init__(self,user_id,username,password_hash,is_admin,is_active):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.is_active = is_active

    def create(username,password_hash):
        return User(0,username,password_hash,False,False)


    def __str__(self):
        return f"{self.user_id} {self.username} {self.password_hash}"




# def load(id:str,db) -> User | None:
#
#     query = database.Query(db)
#
#     data = query.selectById("User","user_id",id)
#
#     if data is None: return None
#
#     user_id,password_hash,username,is_admin = data
#
#     return User(user_id,username,password_hash,is_admin)
#
#
# def loadByUsername(username: str):
#
#     row = database.query.select("User",f"username = \'{username}\'")
#
#     if row is None: return None
#
#     user_id,password_hash,username,is_admin,is_active = row
#
#     return User(user_id,username,password_hash, is_admin,is_active)
#



