import os, time, mysql.connector,sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from mysql.connector import pooling, Error
 
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", 3306)),
    "user":     os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASS", "PASSWORD"),
    "database": os.getenv("DB_NAME", "address_book_db"),
    "auth_plugin": "caching_sha2_password",
}

_pool: pooling.MySQLConnectionPool | None = None

def get_pool():
    global _pool
    if _pool is None:
        _pool = pooling.MySQLConnectionPool(
            pool_name="addr_pool",
            pool_size=5,
            pool_reset_session=True,
            **DB_CONFIG,
        )
    return _pool

def connect(retries: int = 3, delay: float = 2.0):
    """Get a pooled connection with simple retry logic."""
    for attempt in range(1, retries + 1):
        try:
            return get_pool().get_connection()
        except Error as err:
            print(f"DB connect attempt {attempt} failed ➜ {err}")
            time.sleep(delay)
    return None
