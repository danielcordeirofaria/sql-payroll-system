
-- Departments
CREATE TABLE departments (
    id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE
);

-- Job positions
CREATE TABLE positions (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    title       VARCHAR(100)  NOT NULL UNIQUE,
    base_salary NUMERIC(10, 2) NOT NULL CHECK (base_salary > 0)
);

-- Employees
CREATE TABLE employees (
    id            INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name          VARCHAR(150) NOT NULL,
    hire_date     DATE         NOT NULL DEFAULT CURRENT_DATE,
    department_id INTEGER      NOT NULL REFERENCES departments (id),
    position_id   INTEGER      NOT NULL REFERENCES positions (id)
);

-- Monthly benefits
CREATE TABLE benefits (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER        NOT NULL REFERENCES employees (id) ON DELETE CASCADE,
    name        VARCHAR(100)   NOT NULL,
    amount      NUMERIC(10, 2) NOT NULL CHECK (amount > 0)
);

-- One payroll record
CREATE TABLE payroll (
    id          INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id INTEGER        NOT NULL REFERENCES employees (id),
    pay_month   DATE           NOT NULL CHECK (EXTRACT(DAY FROM pay_month) = 1),
    gross_pay   NUMERIC(10, 2) NOT NULL CHECK (gross_pay >= 0),
    UNIQUE (employee_id, pay_month)
);

-- Deductions
CREATE TABLE deductions (
    id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    payroll_id INTEGER        NOT NULL REFERENCES payroll (id) ON DELETE CASCADE,
    name       VARCHAR(100)   NOT NULL,
    amount     NUMERIC(10, 2) NOT NULL CHECK (amount > 0)
);