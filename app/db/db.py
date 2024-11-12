import pymysql.cursors
from db.pool import MySQLConnectionPool

class DB:
    def __init__(self, host, username, password, database):
        self.pool = MySQLConnectionPool(
            host=host,
            user=username,
            password=password,
            database=database
        )
    
    """ 
        * 전체 데이터 목록을 반환합니다.

        ** table : 가져올 데이터 테이블 명

        * 예시
        data = DB.findAll("USER")

        * 반환 타입: dictionary
    """
    def findAll(self, table):
        connection = self.pool.get_connection()  
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = f"SELECT * FROM {table}"
                cursor.execute(query)  
                result = cursor.fetchall() 
            return result
        finally:
            self.pool.return_connection(connection)  

    """ 
        * 데이터의 생성 일시를 기준으로 잘라서 데이터를 반환하는 메서드입니다.
        * start 와 end 사이 시간에 생성된 데이터 목록을 가져옵니다.

        ** table : 가져올 데이터 테이블 명
        ** start : datetime (from datetime import datetime)
        ** end : datetime 

        * 예시

        from datetime import datetime
        data = DB.findByCreatedAtBetween(
            "USER", 
            datetime(2024, 11, 1, 0, 0, 0),
            datetime(2024, 11, 2, 0, 0, 0)
        )

        * 반환 타입: dictionary
    """
    def findByCreatedAtBetween(self, table, start, end):
        connection = self.pool.get_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                query = f"SELECT * FROM {table} WHERE created_at > %s AND created_at < %s"
                cursor.execute(query, (start, end))  # 안전하게 파라미터 바인딩
                result = cursor.fetchall()
            return result
        finally:
            self.pool.return_connection(connection)

    def executeQuery(self, query):
        connection = self.pool.get_connection()  
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query)  
                result = cursor.fetchall() 
            return result
        finally:
            self.pool.return_connection(connection)  