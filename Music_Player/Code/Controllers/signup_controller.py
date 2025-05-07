import bcrypt
from DB.database import Database

class SignupController:
    def __init__(self):
        self.db = Database()

    def register_user(self, username, email, password, birth_date):
        # 비밀번호 해시 처리
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        query = """
        INSERT INTO USER (Uname, Email, Password, Bdate)
        VALUES (%s, %s, %s, %s)
        """
        values = (username, email, hashed_password, birth_date)
        try:
            # 데이터베이스에 사용자 추가
            self.db.execute_query(query, values)
            print("회원 가입이 성공적으로 완료되었습니다.")
            return True
        except Exception as e:
            print(f"회원 가입 실패: {e}")
            return False