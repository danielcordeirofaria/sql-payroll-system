from database import connection


def find_all(conn=None):
    sql = "SELECT id, name FROM departments ORDER BY name"
    with connection(conn) as db:
        return db.execute(sql).fetchall()


def create(name, conn=None):
    sql = """
        INSERT INTO departments (name)
        VALUES (%s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (name,)).fetchone()[0]


def update_name(department_id, name, conn=None):
    sql = """
        UPDATE departments
        SET name = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (name, department_id))


def delete(department_id, conn=None):
    sql = "DELETE FROM departments WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (department_id,))


def salary_statistics(conn=None):
    """
    Shows, for each department, how many employees it has and the
    total and average base salary of those employees.

    Starting from departments (not employees) and using LEFT JOIN
    keeps a department with no employees in the result, with 0 and
    NULL instead of disappearing from the report.

    COUNT(employees.id) counts only real employees. If we used
    COUNT(*), a department with no employees would be counted as 1,
    because the LEFT JOIN still produces one "empty" row for it.
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
