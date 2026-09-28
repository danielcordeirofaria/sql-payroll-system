# SQL Payroll System

# Overview

As a software engineer who frequently uses Java, Spring Boot, and JPA, I often rely on an ORM to generate database queries automatically. I built this project to deepen my understanding of relational databases by writing raw SQL queries by hand and managing database connections and transactions directly.

The SQL Payroll System is a command-line application for managing human resources and monthly payroll records. It connects directly to a PostgreSQL database using Python and the `psycopg` database driver without any ORM. Through an interactive console menu, users can:
- Manage company departments and job positions.
- Register employees, assign them to departments, and update their roles.
- Add and adjust recurring employee benefits (such as health insurance and meal allowances).
- Generate monthly payroll records for all active employees with a single command.
- Add payroll deductions (such as income tax and loan payments).
- View analytical reports, including full monthly net pay summaries, employees without benefits, and department salary statistics.

To run the program:
1. Start the PostgreSQL container:
   ```bash
   docker compose up -d
   ```
2. Create and activate a virtual environment:
   - Windows (PowerShell):
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   - macOS / Linux:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Launch the console application:
   ```bash
   python main.py
   ```

[Software Demo Video](https://www.youtube.com/watch?v=8hbC6CkSlss)

# Relational Database

This project uses PostgreSQL 17 running inside a Docker container. The database schema enforces business rules directly through primary keys, foreign keys, unique constraints, and check constraints across six tables:

- `departments`: Stores department names (`id`, `name`). The `name` column has a `UNIQUE` constraint to prevent duplicate departments.
- `positions`: Holds job titles and baseline compensation (`id`, `title`, `base_salary`). It enforces a positive salary using `CHECK (base_salary > 0)` and requires unique job titles.
- `employees`: Stores worker records (`id`, `name`, `hire_date`, `department_id`, `position_id`). Foreign keys link each employee to a department and a position.
- `benefits`: Stores recurring monthly perks per employee (`id`, `employee_id`, `name`, `amount`). Uses `ON DELETE CASCADE` so benefits are removed automatically if an employee is deleted, and ensures `amount > 0`.
- `payroll`: Represents a monthly pay slip for an employee (`id`, `employee_id`, `pay_month`, `gross_pay`). A `UNIQUE (employee_id, pay_month)` constraint prevents paying the same worker twice in the same month, and a check constraint validates that `pay_month` is always the first day of the month.
- `deductions`: Stores line-item deductions tied to a payroll record (`id`, `payroll_id`, `name`, `amount`). Linked via foreign key with `ON DELETE CASCADE` so deleting a payroll record cleans up its deductions.

The project uses complex SQL queries, including `JOIN`, `LEFT JOIN` (to include records with zero matches, like departments without employees or employees without benefits), `GROUP BY`, aggregate functions (`COUNT`, `SUM`, `AVG`, `ROUND`), and `COALESCE` to handle null values when calculating net pay.

# Development Environment

- Docker and Docker Compose (to run and isolate the PostgreSQL database)
- Visual Studio Code
- Git and GitHub
- Python 3.13
- `psycopg` 3.3 (PostgreSQL database adapter for Python)

# Useful Websites

- [PostgreSQL Official Documentation](https://www.postgresql.org/docs/17/index.html)
- [Psycopg 3 Documentation](https://www.psycopg.org/psycopg3/docs/)
- [PostgreSQL Tutorial](https://www.postgresqltutorial.com/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Docker Hub - Official PostgreSQL Image](https://hub.docker.com/_/postgres)

# Future Work

- Add automatic tax bracket calculations based on salary ranges instead of a flat percentage.
- Export monthly payroll reports to CSV or PDF files.
- Add pagination and search filters for large employee lists.
- Support one-time bonuses and overtime pay calculations.