from database import connection


def find_by_payroll(payroll_id, conn=None):
    sql = """
        SELECT id, name, amount
        FROM deductions
        WHERE payroll_id = %s
        ORDER BY name
    """
    with connection(conn) as db:
        return db.execute(sql, (payroll_id,)).fetchall()


def create(payroll_id, name, amount, conn=None):
    sql = """
        INSERT INTO deductions (payroll_id, name, amount)
        VALUES (%s, %s, %s)
        RETURNING id
    """
    with connection(conn) as db:
        return db.execute(sql, (payroll_id, name, amount)).fetchone()[0]


def update_amount(deduction_id, amount, conn=None):
    sql = """
        UPDATE deductions
        SET amount = %s
        WHERE id = %s
    """
    with connection(conn) as db:
        db.execute(sql, (amount, deduction_id))


def delete(deduction_id, conn=None):
    sql = "DELETE FROM deductions WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (deduction_id,))


if __name__ == "__main__":
    for deduction in find_by_payroll(1):
        print(deduction)
