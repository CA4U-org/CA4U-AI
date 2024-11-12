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
    
    def execute_with_connection(self, query, params=None):
        connection = self.pool.get_connection()
        try:
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)  
                result = cursor.fetchall()
            return result
        finally:
            self.pool.return_connection(connection)

    """
        * findAll(table)
        * table에 해당하는 데이터 목록 전체를 조회합니다.
        * 조회한 결과는 dictionary로 반환됩니다.
        *
        * Ex.
        * from core.ctx import CTX
        *
        * data = CTX.DB.findAll("USER") 
    """
    def findAll(self, table):
        query = f"SELECT * FROM {table}"
        return self.execute_with_connection(query)
    

    """
        * findByCreatedAtBetween(table, start, end)
        * 특정 기간 내에 생성된 데이터의 목록을 조회합니다. 
        * start와 end는 datetime을 사용합니다. 
        *
        * Ex.
        * from datetime import datetime
        * from core.ctx import CTX
        *
        * start_date = datetime(2024,1,1)
        * end_date = datetime(2024,12,31,23,59,59)
        *
        * data = CTX.DB.findByCreatedAtBetween(
        *   "USER", start_date, end_date
        * ) 
        *
        * 조회한 결과는 dictionary로 반환됩니다.
    """
    def findByCreatedAtBetween(self, table, start, end):
        query = f"SELECT * FROM {table} WHERE created_at > %s AND created_at < %s"
        return self.execute_with_connection(query, (start, end))

    def executeQuery(self, query, params=None):
        return self.execute_with_connection(query, params)