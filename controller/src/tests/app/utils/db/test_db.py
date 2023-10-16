from unittest import mock
from app.utils.db.db import DatabaseConnectionManager 

@mock.patch('app.utils.db.db.psycopg2.pool.SimpleConnectionPool', autospec=True)
def test_singleton_pattern(mock_connection_pool):
    instance1 = DatabaseConnectionManager()
    instance2 = DatabaseConnectionManager()
    instance3 = DatabaseConnectionManager()

    assert mock_connection_pool.call_count == 1, "SimpleConnectionPool was initialized more than once"

    assert instance1 is instance2 is instance3, "DatabaseConnectionManager is not following the Singleton pattern"
    assert instance1._connection_pool is instance2._connection_pool is instance3._connection_pool, "Connection pools of instances do not match"
