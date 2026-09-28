BEGIN;

-- Departments
INSERT INTO departments (name) VALUES
    ('Human Resources'),
    ('Information Technology'),
    ('Finance'),
    ('Sales'),
    ('Marketing');

-- Job positions
INSERT INTO positions (title, base_salary) VALUES
    ('HR Analyst',                4500.00),
    ('Software Developer',        8000.00),
    ('Senior Software Developer', 12000.00),
    ('Accountant',                5500.00),
    ('Sales Representative',      3500.00),
    ('Manager',                   15000.00);

-- Employees
INSERT INTO employees (name, hire_date, department_id, position_id)
SELECT employee_data.name, employee_data.hire_date::date, departments.id, positions.id
FROM (VALUES
    ('Ana Souza',      '2022-03-01', 'Human Resources',        'HR Analyst'),
    ('Bruno Lima',     '2021-07-15', 'Information Technology', 'Senior Software Developer'),
    ('Carla Mendes',   '2023-01-10', 'Information Technology', 'Software Developer'),
    ('Diego Rocha',    '2024-05-20', 'Information Technology', 'Software Developer'),
    ('Elisa Martins',  '2020-11-02', 'Finance',                'Accountant'),
    ('Fabio Costa',    '2019-04-08', 'Finance',                'Manager'),
    ('Gabriela Alves', '2025-02-17', 'Sales',                  'Sales Representative'),
    ('Henrique Dias',  '2026-08-03', 'Sales',                  'Sales Representative')
) AS employee_data (name, hire_date, department, position)
JOIN departments ON departments.name = employee_data.department
JOIN positions   ON positions.title  = employee_data.position;

-- Monthly benefits
INSERT INTO benefits (employee_id, name, amount)
SELECT employees.id, benefit_data.benefit, benefit_data.amount
FROM (VALUES
    ('Ana Souza',      'Meal card',             600.00),
    ('Ana Souza',      'Health plan',           350.00),
    ('Bruno Lima',     'Meal card',             600.00),
    ('Bruno Lima',     'Health plan',           350.00),
    ('Bruno Lima',     'Remote work allowance', 200.00),
    ('Carla Mendes',   'Meal card',             600.00),
    ('Elisa Martins',  'Meal card',             600.00),
    ('Elisa Martins',  'Health plan',           350.00),
    ('Fabio Costa',    'Meal card',             600.00),
    ('Fabio Costa',    'Health plan',           350.00),
    ('Fabio Costa',    'Car allowance',         800.00),
    ('Gabriela Alves', 'Meal card',             600.00)
) AS benefit_data (employee, benefit, amount)
JOIN employees ON employees.name = benefit_data.employee;

-- Payroll: August 2026
INSERT INTO payroll (employee_id, pay_month, gross_pay)
SELECT employees.id, DATE '2026-08-01', positions.base_salary
FROM employees
JOIN positions ON positions.id = employees.position_id
WHERE employees.hire_date < DATE '2026-08-01';

-- Payroll: September 2026
INSERT INTO payroll (employee_id, pay_month, gross_pay)
SELECT employees.id, DATE '2026-09-01', positions.base_salary
FROM employees
JOIN positions ON positions.id = employees.position_id
WHERE employees.hire_date < DATE '2026-09-01';

-- Income tax (15%)
INSERT INTO deductions (payroll_id, name, amount)
SELECT payroll.id, 'Income tax', ROUND(payroll.gross_pay * 0.15, 2)
FROM payroll;

-- Other deductions
INSERT INTO deductions (payroll_id, name, amount)
SELECT payroll.id, deduction_data.deduction, deduction_data.amount
FROM (VALUES
    ('Bruno Lima',   DATE '2026-09-01', 'Loan payment',   500.00),
    ('Carla Mendes', DATE '2026-08-01', 'Unpaid absence', 250.00),
    ('Fabio Costa',  DATE '2026-09-01', 'Loan payment',   1000.00)
) AS deduction_data (employee, pay_month, deduction, amount)
JOIN employees ON employees.name = deduction_data.employee
JOIN payroll   ON payroll.employee_id = employees.id
              AND payroll.pay_month   = deduction_data.pay_month;

COMMIT;
