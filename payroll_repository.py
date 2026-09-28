from database import connection


def generate_for_month(pay_month, conn=None):
    """Creates one payroll record for every employee hired before this month."""
    sql = """
        INSERT INTO payroll (employee_id, pay_month, gross_pay)
        SELECT employees.id, %s, positions.base_salary
        FROM employees
        JOIN positions ON positions.id = employees.position_id
        WHERE employees.hire_date < %s
    """
    with connection(conn) as db:
        db.execute(sql, (pay_month, pay_month))


def find_by_employee(employee_id, conn=None):

    """Returns all payroll records of one employee."""
    
    sql = """
        SELECT id, pay_month, gross_pay
        FROM payroll
        WHERE employee_id = %s
        ORDER BY pay_month
    """
    with connection(conn) as db:
        return db.execute(sql, (employee_id,)).fetchall()


def monthly_report(pay_month, conn=None):
    """
    Shows the full payroll of a month: for each employee, the gross
    pay, the total benefits, the total deductions, and the net pay.

    net_pay = gross_pay + total_benefits - total_deductions
    """
    sql = """
        SELECT
            employees.name,
            payroll.gross_pay,
            COALESCE(benefit_totals.total, 0)   AS total_benefits,
            COALESCE(deduction_totals.total, 0) AS total_deductions,
            payroll.gross_pay
                + COALESCE(benefit_totals.total, 0)
                - COALESCE(deduction_totals.total, 0) AS net_pay
        FROM payroll
        JOIN employees ON employees.id = payroll.employee_id
        LEFT JOIN (
            SELECT employee_id, SUM(amount) AS total
            FROM benefits
            GROUP BY employee_id
        ) AS benefit_totals ON benefit_totals.employee_id = payroll.employee_id
        LEFT JOIN (
            SELECT payroll_id, SUM(amount) AS total
            FROM deductions
            GROUP BY payroll_id
        ) AS deduction_totals ON deduction_totals.payroll_id = payroll.id
        WHERE payroll.pay_month = %s
        ORDER BY employees.name
    """
    with connection(conn) as db:
        return db.execute(sql, (pay_month,)).fetchall()


# There is no update function here on purpose. A payroll record is a
# historical fact: it shows what the employee was paid in that month.
# Changing gross_pay later would rewrite history. A real correction
# would be a new adjustment record, not an edit of the old one.


def delete(payroll_id, conn=None):
    """Removes one payroll record from the database."""
    sql = "DELETE FROM payroll WHERE id = %s"
    with connection(conn) as db:
        db.execute(sql, (payroll_id,))


if __name__ == "__main__":
    for row in monthly_report("2026-09-01"):
        print(row)
