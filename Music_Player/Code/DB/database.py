import pymysql

class Database:
    _instance = None

    def __new__(cls, *args, **kargs):
        # 이미 생성된 인스턴스가 있으면 해당 인스턴스를 반환
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, host='localhost', user='root', password='본인패스워드', database='Music', port=3306):
        
        if hasattr(self, "connection"):
            return
        
        #Mysql 연결 설정
        try:
            self.connection = pymysql.connect(
                host = host,
                user = user,
                password = password,
                database = database,
                port = port,
                charset = "utf8mb4",
                cursorclass= pymysql.cursors.DictCursor 

            )
            print("데이터베이스 연결 성공")
        except pymysql.MySQLError as e:
            print("데이터베이스 연결 실패: {e}")
            self.connection = None
    
    def execute_query(self, query, params=()):
        with self.connection.cursor() as cursor:
            cursor.execute(query, params)
            self.connection.commit()
            return cursor.fetchall()  #query result
        
    def close(self):
        if self.connection:
            self.connection.close()

    def get_last_insert_id(self):
        # 최근에 삽입된 auto_increment 값 반환
        with self.connection.cursor()as cursor:
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchone()
            return result['LAST_INSERT_ID()'] # 삽입이 없으면 0을 반환
        
        
