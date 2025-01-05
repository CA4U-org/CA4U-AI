import pymysql
import queue

class MySQLConnectionPool:
    def __init__(self, host, user, password, database, pool_size=1):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.pool_size = pool_size
        self.pool = queue.Queue(maxsize=pool_size)

        for _ in range(pool_size):
            connection = self.create_connection()
            self.pool.put(connection)
        print("Database Connection Pool Initiated.")
        print("Connection Size :" + str(pool_size))

    def create_connection(self):
        return pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

    def get_connection(self, timeout=30):
        try:
            connection = self.pool.get(timeout=timeout)
            return connection
        except queue.Empty:
            raise TimeoutError("Failed to get connection.")

    def return_connection(self, connection):
        self.pool.put(connection)

    def close_all_connections(self):
        while not self.pool.empty():
            connection = self.pool.get()
            connection.close()