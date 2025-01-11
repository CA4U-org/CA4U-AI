import pymysql.cursors
from db.pool import MySQLConnectionPool
class DB:
    def __init__(self, host, username, password, database):
        # MySQLConnectionPool 생성
        self.pool = MySQLConnectionPool(
            host=host,
            user=username,
            password=password,
            database=database
        )
    def execute_with_connection(self, query, params=None):
        # 새로운 세션을 생성하고 쿼리 실행
        connection = self.pool.get_connection()
        try:
            connection.ping(reconnect=True)  # 연결 강제 확인
            connection.autocommit(True)  # Autocommit 활성화
            self._start_session(connection)  # 세션 시작
            with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                cursor.execute(query, params)
                result = cursor.fetchall()
            return result
        finally:
            self._end_session(connection)  # 세션 종료
            self.pool.return_connection(connection)  # 커넥션 반환
    def _start_session(self, connection):
        """
        세션 시작 로직: 트랜잭션 격리 수준 설정 등 세션 초기화.
        """
        with connection.cursor() as cursor:
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;")
            cursor.execute("START TRANSACTION;")  # 세션 트랜잭션 시작
    def _end_session(self, connection):
        """
        세션 종료 로직: 트랜잭션 커밋 및 세션 초기화.
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute("COMMIT;")  # 트랜잭션 커밋
        except Exception:
            with connection.cursor() as cursor:
                cursor.execute("ROLLBACK;")  # 실패 시 롤백
    def find_all(self, table):
        """
        테이블 전체 데이터를 조회하는 메서드.
        """
        query = f"SELECT SQL_NO_CACHE * FROM {table}"  # Query Cache 우회
        return self.execute_with_connection(query)
    def find_by_created_at_between(self, table, start, end):
        """
        특정 기간 내 데이터 조회.
        """
        query = f"SELECT * FROM {table} WHERE created_at > %s AND created_at < %s"
        return self.execute_with_connection(query, (start, end))
    def execute_query(self, query, params=None):
        """
        임의 쿼리 실행 메서드.
        """
        return self.execute_with_connection(query, params)