from contextlib import contextmanager

import psycopg

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "payroll",
    "user": "payroll",
    "password": "payroll",
}


def get_connection():
    return psycopg.connect(**DB_CONFIG)


@contextmanager
def connection(conn=None):
    if conn is not None:
        yield conn
    else:
        with get_connection() as own_conn:
            yield own_conn


if __name__ == "__main__":
    with get_connection() as conn:
        result = conn.execute("SELECT COUNT(*) FROM employees").fetchone()
        print(f"Connected. Employees in database: {result[0]}")
