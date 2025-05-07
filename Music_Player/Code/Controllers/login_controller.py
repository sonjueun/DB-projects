import bcrypt
from DB.database import Database

class LoginController:
    def __init__(self):
        self.db = Database()
    def authenticate(self, email, password):
        # db에서 사용자 정보 확인
        query = "SELECT * FROM USER WHERE email = %s"
        result = self.db.execute_query(query, (email, ))
        if result:
            hashed_password = result[0]['Password']

            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                return result[0]
        return None
    