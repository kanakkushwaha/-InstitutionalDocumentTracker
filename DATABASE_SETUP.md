# Database Setup

This project currently runs in the app with SQLite by default, but full raw MySQL DBMS files are now included for ER modeling, normalization, DDL, DML, joins, views, procedures, cursor, and triggers.

## Files

- `dbms/01_problem_er_normalization.md`
  Contains:
  - problem statement
  - ER modeling explanation
  - relational conversion
  - normalization

- `dbms/02_schema_mysql.sql`
  Creates:
  - `departments`
  - `admin`
  - `placement_cell`
  - `scholarship_cell`
  - `students`
  - `teachers`
  - `documents`
  - `notifications`
  - `document_audit`
  - indexes and constraints

- `dbms/03_seed_mysql.sql`
  Inserts demo data.

- `dbms/04_dml_queries.sql`
  Contains 10+ DML queries using insert, select, update, delete, operators, functions, and set operator.

- `dbms/05_joins_subqueries_views.sql`
  Contains 10+ queries using joins, subqueries, views, group by, and having.

- `dbms/06_procedures_functions.sql`
  Contains stored procedures and functions.

- `dbms/07_cursor_and_triggers.sql`
  Contains cursor code, control structures, exception handling, and triggers.

## How To Use In MySQL Workbench

1. Open MySQL Workbench.
2. Connect to your MySQL server.
3. Open and run `dbms/02_schema_mysql.sql`.
4. Open and run `dbms/03_seed_mysql.sql`.
5. Run other SQL files one by one as per syllabus requirement.
6. Refresh the schema navigator.
7. You should now see:
   - `institutional_document_tracker`
   - tables: `departments`, `admin`, `placement_cell`, `scholarship_cell`, `students`, `teachers`, `documents`, `notifications`, `document_audit`

## Notes

- The Flask app is currently configured to use SQLite by default in `config.py`.
- The SQL files are designed to match your ER-style DBMS presentation and syllabus requirements more closely.
- If you want, the next step can be switching the live app from SQLite to MySQL so the app and Workbench use the same database.
