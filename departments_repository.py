from database import connection


def find_all(conn=None):

    """Returns every department."""

    sql = "SELECT id, name FROM departments ORDER BY name"
    with connection(conn) as db:
        return db.execute(sql).fetchall()


def create(name, conn=None):

    """Adds a new department and returns its new id."""

    sql = """
        INSERT INTO departments (name)
        VALUES (%s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (name,)).fetchone()[0]


def update_name(department_id, name, conn=None):
    """Changes the name of one department."""
    sql = """
        UPDATE departments
        SET name = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (name, department_id))


def delete(department_id, conn=None):

    """Removes one department from the database."""
    
    sql = "DELETE FROM departments WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (department_id,))


def salary_statistics(conn=None):
    """
    Returns a list of departments with the number of employees, total salary, and average salary.
    """
    sql = """
        SELECT
            departments.name AS department,
            COUNT(employees.id)        AS employee_count,
            SUM(positions.base_salary) AS total_salary,
            ROUND(AVG(positions.base_salary), 2) AS average_salary
        FROM departments
        LEFT JOIN employees ON employees.department_id = departments.id
        LEFT JOIN positions ON positions.id = employees.position_id
        GROUP BY departments.name
        ORDER BY departments.name
    """
    with connection(conn) as db:
        return db.execute(sql).fetchall()


if __name__ == "__main__":
    for department in find_all():
        print(department)
