import os
import psycopg2
from psycopg2 import pool
from threading import Lock


class DatabaseConnectionManager:
    """
    Connection pool manager in Singleton pattern. 

    Lock is used to ensure that only one instance of the class is created.
    """
    _instance = None
    _lock = Lock()
    _connection_pool = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(DatabaseConnectionManager, cls).__new__(cls)
                minconn = int(os.getenv("DB_MINCONN", "1"))
                maxconn = int(os.getenv("DB_MAXCONN", "10"))
                host = os.getenv("DB_HOST", "postgres")
                port = os.getenv("DB_PORT", "5432")
                dbname = os.getenv("DB_NAME", "postgres")
                user = os.getenv("DB_USER", "postgres")
                password = os.getenv("DB_PASSWORD", "postgres")
                cls._connection_pool = psycopg2.pool.SimpleConnectionPool(
                    minconn,
                    maxconn,
                    host=host,
                    port=port,
                    dbname=dbname,
                    user=user,
                    password=password,
                )
        return cls._instance

    def __enter__(self):
        self.connection = self._connection_pool.getconn()
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.connection.rollback()
        else:
            self.connection.commit()
        self.cursor.close()
        self._connection_pool.putconn(self.connection)


def get_db_cursor():
    return DatabaseConnectionManager()
