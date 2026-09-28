from database import connection


def find_all(conn=None):
    sql = "SELECT id, title, base_salary FROM positions ORDER BY title"
    with connection(conn) as db:
        return db.execute(sql).fetchall()


def create(title, base_salary, conn=None):
    sql = """
        INSERT INTO positions (title, base_salary)
        VALUES (%s, %s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (title, base_salary)).fetchone()[0]


def update_base_salary(position_id, base_salary, conn=None):
    sql = """
        UPDATE positions
        SET base_salary = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (base_salary, position_id))


def delete(position_id, conn=None):
    sql = "DELETE FROM positions WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (position_id,))


if __name__ == "__main__":
    for position in find_all():
        print(position)
