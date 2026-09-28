from database import connection


def find_by_employee(employee_id, conn=None):
    sql = """
        SELECT id, name, amount
        FROM benefits
        WHERE employee_id = %s
        ORDER BY name
    """
    with connection(conn) as db:
        return db.execute(sql, (employee_id,)).fetchall()


def create(employee_id, name, amount, conn=None):
    sql = """
        INSERT INTO benefits (employee_id, name, amount)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (employee_id, name, amount)).fetchone()[0]


def update_amount(benefit_id, amount, conn=None):
    sql = """
        UPDATE benefits
        SET amount = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (amount, benefit_id))


def delete(benefit_id, conn=None):
    sql = "DELETE FROM benefits WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (benefit_id,))


def find_employees_without_benefits(conn=None):
    """
    Finds employees who have no benefit at all.

    The LEFT JOIN keeps every employee, even the ones with no row in
    benefits. For those, all benefits columns come back as NULL.
    WHERE benefits.id IS NULL then keeps only that group.
    """
    sql = """
        SELECT employees.name, departments.name AS department
        FROM employees
        LEFT JOIN benefits ON benefits.employee_id = employees.id
        JOIN departments ON departments.id = employees.department_id
        WHERE benefits.id IS NULL
        ORDER BY employees.name
    """
    with connection(conn) as db:
        return db.execute(sql).fetchall()


if __name__ == "__main__":
    for employee in find_employees_without_benefits():
        print(employee)
