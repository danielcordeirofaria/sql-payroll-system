from database import connection


def find_all(conn=None):

    """Returns every employee, with department name and position title."""

    sql = """
        SELECT employees.id,
               employees.name,
               employees.hire_date,
               departments.name AS department,
               positions.title  AS position
        FROM employees
        JOIN departments ON departments.id = employees.department_id
        JOIN positions   ON positions.id   = employees.position_id
        ORDER BY employees.name
    """
    with connection(conn) as db:
        return db.execute(sql).fetchall()


def create(name, hire_date, department_id, position_id, conn=None):

    """Adds a new employee and returns the new employee id."""
    
    sql = """
        INSERT INTO employees (name, hire_date, department_id, position_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (name, hire_date, department_id, position_id)).fetchone()[0]


def update_position(employee_id, position_id, conn=None):
    """Changes the position of one employee."""
    sql = """
        UPDATE employees
        SET position_id = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (position_id, employee_id))


def delete(employee_id, conn=None):
    """Removes one employee from the database."""
    sql = "DELETE FROM employees WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (employee_id,))


if __name__ == "__main__":
    for employee in find_all():
        print(employee)
