"""Console menu for the HR/Payroll Management System."""

import psycopg

import benefits_repository
import deductions_repository
import departments_repository
import employee_repository
import payroll_repository
import positions_repository


def read_int(prompt):
    """Reads a number from the user. Keeps asking until it gets one."""
    while True:
        value = input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Please enter a number.")


def read_amount(prompt):
    """Reads a money value from the user. Keeps asking until it gets one."""
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Please enter a number, like 500 or 500.00.")


def run_safely(action):
    """
    Runs a database action and shows a clear message if it fails.

    This catches errors like a foreign key or a check constraint
    violation, so the program shows a message instead of crashing.
    The connection used by the action already rolled itself back,
    so the program can keep running normally after this.

    Returns True if the action ran without error, False otherwise.
    The caller uses this to decide whether to print a success message.
    """
    try:
        action()
        return True
    except psycopg.Error as error:
        print(f"\nThe database rejected this operation: {error.diag.message_primary}")
        return False


# --- Employees -------------------------------------------------------

def list_employees():

    """Prints every employee in a simple table."""
    
    print("\nID  Name                Hire date   Department               Position")
    for employee in employee_repository.find_all():
        id_, name, hire_date, department, position = employee
        print(f"{id_:<4}{name:<20}{str(hire_date):<12}{department:<25}{position}")


def choose_department():
    """Shows all departments and asks the user to pick one by id."""
    print("\nDepartments:")
    for department_id, name in departments_repository.find_all():
        print(f"  {department_id}. {name}")
    return read_int("Department id: ")


def choose_position():
    """Shows all positions and asks the user to pick one by id."""
    print("\nPositions:")
    for position_id, title, base_salary in positions_repository.find_all():
        print(f"  {position_id}. {title} (base salary: {base_salary})")
    return read_int("Position id: ")


def add_employee():
    """Asks for the new employee data and saves it."""
    name = input("Employee name: ")
    hire_date = input("Hire date (YYYY-MM-DD): ")
    department_id = choose_department()
    position_id = choose_position()

    def action():
        new_id = employee_repository.create(name, hire_date, department_id, position_id)
        print(f"Employee created with id {new_id}.")

    run_safely(action)


def change_employee_position():
    """Asks for an employee and a new position, then updates it."""
    list_employees()
    employee_id = read_int("\nEmployee id: ")
    position_id = choose_position()
    if run_safely(lambda: employee_repository.update_position(employee_id, position_id)):
        print("Position updated.")


def remove_employee():
    """Asks for an employee id and removes that employee."""
    list_employees()
    employee_id = read_int("\nEmployee id to remove: ")
    if run_safely(lambda: employee_repository.delete(employee_id)):
        print("Employee removed.")


def employees_menu():
    """Shows the Employees menu and runs the option the user picks."""
    while True:
        print("\n--- Employees ---")
        print("1. List employees")
        print("2. Add employee")
        print("3. Change employee position")
        print("4. Remove employee")
        print("0. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            list_employees()
        elif choice == "2":
            add_employee()
        elif choice == "3":
            change_employee_position()
        elif choice == "4":
            remove_employee()
        elif choice == "0":
            return
        else:
            print("Invalid option.")


# --- Benefits ----------------------------------------------------------

def list_benefits():
    """Asks for an employee and prints all of their benefits."""
    list_employees()
    employee_id = read_int("\nEmployee id: ")
    print("\nID  Name                     Amount")
    for benefit_id, name, amount in benefits_repository.find_by_employee(employee_id):
        print(f"{benefit_id:<4}{name:<25}{amount}")


def add_benefit():
    """Asks for a benefit and adds it to an employee."""
    list_employees()
    employee_id = read_int("\nEmployee id: ")
    name = input("Benefit name: ")
    amount = read_amount("Amount: ")

    def action():
        new_id = benefits_repository.create(employee_id, name, amount)
        print(f"Benefit created with id {new_id}.")

    run_safely(action)


def update_benefit_amount():
    """Asks for a benefit id and a new amount, then updates it."""
    benefit_id = read_int("Benefit id: ")
    amount = read_amount("New amount: ")
    if run_safely(lambda: benefits_repository.update_amount(benefit_id, amount)):
        print("Benefit updated.")


def remove_benefit():
    """Asks for a benefit id and removes it."""
    benefit_id = read_int("Benefit id to remove: ")
    if run_safely(lambda: benefits_repository.delete(benefit_id)):
        print("Benefit removed.")


def benefits_menu():
    """Shows the Benefits menu and runs the option the user picks."""
    while True:
        print("\n--- Benefits ---")
        print("1. List benefits of an employee")
        print("2. Add benefit")
        print("3. Update benefit amount")
        print("4. Remove benefit")
        print("0. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            list_benefits()
        elif choice == "2":
            add_benefit()
        elif choice == "3":
            update_benefit_amount()
        elif choice == "4":
            remove_benefit()
        elif choice == "0":
            return
        else:
            print("Invalid option.")


# --- Payroll -------------------------------------------------------------

def generate_payroll():
    """Asks for a month and creates payroll records for that month."""
    pay_month = input("Month to generate (YYYY-MM-01): ")
    if run_safely(lambda: payroll_repository.generate_for_month(pay_month)):
        print("Payroll generated.")


def list_payroll_by_employee():
    """Asks for an employee and prints all of their payroll records."""
    list_employees()
    employee_id = read_int("\nEmployee id: ")
    print("\nID  Month       Gross pay")
    for payroll_id, pay_month, gross_pay in payroll_repository.find_by_employee(employee_id):
        print(f"{payroll_id:<4}{str(pay_month):<12}{gross_pay}")


def add_deduction():
    """Asks for a deduction and adds it to a payroll record."""
    payroll_id = read_int("Payroll id: ")
    name = input("Deduction name: ")
    amount = read_amount("Amount: ")

    def action():
        new_id = deductions_repository.create(payroll_id, name, amount)
        print(f"Deduction created with id {new_id}.")

    run_safely(action)


def list_deductions():
    """Asks for a payroll id and prints all of its deductions."""
    payroll_id = read_int("Payroll id: ")
    print("\nID  Name                     Amount")
    for deduction_id, name, amount in deductions_repository.find_by_payroll(payroll_id):
        print(f"{deduction_id:<4}{name:<25}{amount}")


def update_deduction_amount():
    """Asks for a deduction id and a new amount, then updates it."""
    deduction_id = read_int("Deduction id: ")
    amount = read_amount("New amount: ")
    if run_safely(lambda: deductions_repository.update_amount(deduction_id, amount)):
        print("Deduction updated.")


def remove_deduction():
    """Asks for a deduction id and removes it."""
    deduction_id = read_int("Deduction id to remove: ")
    if run_safely(lambda: deductions_repository.delete(deduction_id)):
        print("Deduction removed.")


def remove_payroll():
    """Asks for a payroll id and removes that payroll record."""
    payroll_id = read_int("Payroll id to remove: ")
    if run_safely(lambda: payroll_repository.delete(payroll_id)):
        print("Payroll record removed.")


def payroll_menu():
    """Shows the Payroll menu and runs the option the user picks."""
    while True:
        print("\n--- Payroll ---")
        print("1. Generate payroll for a month")
        print("2. List payroll of an employee")
        print("3. Add deduction")
        print("4. List deductions of a payroll record")
        print("5. Update deduction amount")
        print("6. Remove deduction")
        print("7. Remove payroll record")
        print("0. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            generate_payroll()
        elif choice == "2":
            list_payroll_by_employee()
        elif choice == "3":
            add_deduction()
        elif choice == "4":
            list_deductions()
        elif choice == "5":
            update_deduction_amount()
        elif choice == "6":
            remove_deduction()
        elif choice == "7":
            remove_payroll()
        elif choice == "0":
            return
        else:
            print("Invalid option.")


# --- Reports ---------------------------------------------------------

def monthly_payroll_report():
    """Asks for a month and prints the full payroll report for it."""
    pay_month = input("Month to report (YYYY-MM-01): ")
    print("\nName                Gross pay   Benefits    Deductions  Net pay")
    for row in payroll_repository.monthly_report(pay_month):
        name, gross_pay, total_benefits, total_deductions, net_pay = row
        print(f"{name:<20}{gross_pay:<12}{total_benefits:<12}{total_deductions:<12}{net_pay}")


def employees_without_benefits_report():
    """Prints every employee who has no benefit."""
    print("\nName                Department")
    for name, department in benefits_repository.find_employees_without_benefits():
        print(f"{name:<20}{department}")


def department_salary_report():
    """Prints salary totals and averages for each department."""
    print("\nDepartment               Employees   Total salary   Average salary")
    for row in departments_repository.salary_statistics():
        department, employee_count, total_salary, average_salary = row
        total_salary = total_salary if total_salary is not None else 0
        average_salary = average_salary if average_salary is not None else 0
        print(f"{department:<25}{employee_count:<12}{total_salary:<15}{average_salary}")


def reports_menu():
    """Shows the Reports menu and runs the option the user picks."""
    while True:
        print("\n--- Reports ---")
        print("1. Monthly payroll report")
        print("2. Employees without benefits")
        print("3. Department salary statistics")
        print("0. Back")
        choice = input("Choose an option: ")

        if choice == "1":
            monthly_payroll_report()
        elif choice == "2":
            employees_without_benefits_report()
        elif choice == "3":
            department_salary_report()
        elif choice == "0":
            return
        else:
            print("Invalid option.")


# --- Main menu -------------------------------------------------------

def main():
    """Shows the main menu and runs the program until the user exits."""
    while True:
        print("\n=== HR/Payroll System ===")
        print("1. Employees")
        print("2. Benefits")
        print("3. Payroll")
        print("4. Reports")
        print("0. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            employees_menu()
        elif choice == "2":
            benefits_menu()
        elif choice == "3":
            payroll_menu()
        elif choice == "4":
            reports_menu()
        elif choice == "0":
            print("Goodbye!")
            return
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()
