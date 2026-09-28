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
    """Opens a new connection to the payroll database."""
    return psycopg.connect(**DB_CONFIG)


@contextmanager
def connection(conn=None):
    
    """Gives a connection to use. Reuses one if given, or opens a new one."""

    if conn is not None:
        yield conn
    else:
        with get_connection() as own_conn:
            yield own_conn


if __name__ == "__main__":
    with get_connection() as conn:
        result = conn.execute("SELECT COUNT(*) FROM employees").fetchone()
        print(f"Connected. Employees in database: {result[0]}")
