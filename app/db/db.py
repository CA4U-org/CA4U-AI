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

    def findAll(self, table):
        query = f"SELECT * FROM {table}"
        return self.execute_with_connection(query)

    def findByCreatedAtBetween(self, table, start, end):
        query = f"SELECT * FROM {table} WHERE created_at > %s AND created_at < %s"
        return self.execute_with_connection(query, (start, end))

    def executeQuery(self, query, params=None):
        return self.execute_with_connection(query, params)