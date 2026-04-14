from functools import lru_cache

from sqlalchemy import inspect, text

from app import db

ROLE_TABLE_MAP = {
    "student": "students",
    "teacher": "teachers",
    "admin": "admin",
    "placement": "placement_cell",
    "scholarship": "scholarship_cell",
}

ROLE_DISPLAY_MAP = {
    "teacher": "Teacher",
    "admin": "System Admin",
    "placement": "Placement Cell",
    "scholarship": "Scholarship Cell",
}


def prune_workbench_users(valid_role_emails):
    tables = _table_lookup()
    for role, allowed_emails in valid_role_emails.items():
        target_key = ROLE_TABLE_MAP.get(role)
        table_name = tables.get(target_key) if target_key else None
        if not table_name:
            continue

        columns = _column_lookup(table_name)
        email_column = _pick_column(columns, "email_id", "email")

        db.session.execute(
            text(
                f"DELETE FROM {table_name} "
                f"WHERE {email_column} LIKE :legacy_pattern"
            ),
            {"legacy_pattern": "%@institution.edu"},
        )

        if allowed_emails:
            placeholders = ", ".join(f":email_{index}" for index, _ in enumerate(allowed_emails))
            params = {f"email_{index}": email for index, email in enumerate(allowed_emails)}
            db.session.execute(
                text(
                    f"DELETE FROM {table_name} "
                    f"WHERE {email_column} NOT IN ({placeholders})"
                ),
                params,
            )


@lru_cache(maxsize=1)
def _table_lookup():
    inspector = inspect(db.engine)
    tables = {name.lower(): name for name in inspector.get_table_names()}
    return {
        "departments": tables.get("departments"),
        "students": tables.get("students"),
        "teachers": tables.get("teachers"),
        "admin": tables.get("admin"),
        "placement_cell": tables.get("placement_cell"),
        "scholarship_cell": tables.get("scholarship_cell"),
    }


@lru_cache(maxsize=None)
def _column_lookup(table_name):
    inspector = inspect(db.engine)
    columns = {column["name"].lower(): column["name"] for column in inspector.get_columns(table_name)}
    return columns


def reset_workbench_sync_cache():
    _table_lookup.cache_clear()
    _column_lookup.cache_clear()


def ensure_workbench_tables():
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS admin (
                Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Role VARCHAR(50) NOT NULL,
                Email_ID VARCHAR(120) NOT NULL UNIQUE,
                Contact_Number VARCHAR(20) NOT NULL,
                Department_ID INT NULL,
                Password VARCHAR(255),
                FOREIGN KEY (Department_ID) REFERENCES departments(id)
                    ON DELETE SET NULL
            )
            """
        )
    )
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS teachers (
                Teacher_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Email_ID VARCHAR(120) NOT NULL UNIQUE,
                Contact_Number VARCHAR(20) NOT NULL,
                Department_ID INT NULL,
                Role VARCHAR(50),
                Password VARCHAR(255),
                FOREIGN KEY (Department_ID) REFERENCES departments(id)
                    ON DELETE SET NULL
            )
            """
        )
    )
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS students (
                PRN VARCHAR(30) PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Class VARCHAR(50) NOT NULL,
                Email_ID VARCHAR(120) NOT NULL UNIQUE,
                Contact_Number VARCHAR(20) NOT NULL,
                Department_ID INT NULL,
                Current_Year VARCHAR(30),
                Password VARCHAR(255),
                FOREIGN KEY (Department_ID) REFERENCES departments(id)
                    ON DELETE SET NULL
            )
            """
        )
    )
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS placement_cell (
                Placement_Cell_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Role VARCHAR(50) NOT NULL,
                Email_ID VARCHAR(120) NOT NULL UNIQUE,
                Contact_Number VARCHAR(20) NOT NULL,
                Department_ID INT NULL,
                Password VARCHAR(255),
                FOREIGN KEY (Department_ID) REFERENCES departments(id)
                    ON DELETE SET NULL
            )
            """
        )
    )
    db.session.execute(
        text(
            """
            CREATE TABLE IF NOT EXISTS scholarship_cell (
                Scholarship_Cell_ID INT AUTO_INCREMENT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Role VARCHAR(50) NOT NULL,
                Email_ID VARCHAR(120) NOT NULL UNIQUE,
                Contact_Number VARCHAR(20) NOT NULL,
                Department_ID INT NULL,
                Password VARCHAR(255),
                FOREIGN KEY (Department_ID) REFERENCES departments(id)
                    ON DELETE SET NULL
            )
            """
        )
    )
    reset_workbench_sync_cache()


def sync_workbench_user(user):
    tables = _table_lookup()
    target_key = ROLE_TABLE_MAP.get(user.role)
    target_table = tables.get(target_key) if target_key else None
    if not target_table:
        return

    department_id = _sync_department(user.department.name if user.department else None, tables)

    if user.role == "student":
        _sync_student(user, department_id, target_table)
        return

    _sync_role_directory(user, department_id, target_table, ROLE_DISPLAY_MAP.get(user.role, user.role.title()))


def _sync_department(department_name, tables):
    department_table = tables.get("departments")
    if not department_table or not department_name:
        return None

    columns = _column_lookup(department_table)
    id_column = _pick_column(columns, "department_id", "id")
    name_column = _pick_column(columns, "department_name", "name")

    existing = db.session.execute(
        text(
            f"SELECT {id_column} FROM {department_table} "
            f"WHERE {name_column} = :name LIMIT 1"
        ),
        {"name": department_name},
    ).fetchone()
    if existing:
        return existing[0]

    db.session.execute(
        text(f"INSERT INTO {department_table} ({name_column}) VALUES (:name)"),
        {"name": department_name},
    )
    created = db.session.execute(
        text(
            f"SELECT {id_column} FROM {department_table} "
            f"WHERE {name_column} = :name LIMIT 1"
        ),
        {"name": department_name},
    ).fetchone()
    return created[0] if created else None


def _sync_student(user, department_id, table_name):
    columns = _column_lookup(table_name)
    prn_column = _pick_column(columns, "prn")
    name_column = _pick_column(columns, "name")
    class_column = _pick_column(columns, "class")
    email_column = _pick_column(columns, "email_id", "email")
    contact_column = _pick_column(columns, "contact_number")
    department_column = _pick_column(columns, "department_id")
    year_column = _pick_column(columns, "current_year")
    password_column = _pick_column(columns, "password")
    current_year = _get_study_year_label(user.prn)
    class_name = _get_class_label(current_year)
    params = {
        "prn": user.prn,
        "name": user.name,
        "class_name": class_name,
        "email": user.email,
        "contact_number": user.contact_number or "",
        "department_id": department_id,
        "current_year": current_year,
        "password": user.password_hash,
    }

    # Replace any stale row that conflicts on either PRN or email before inserting the fresh synced record.
    db.session.execute(
        text(
            f"DELETE FROM {table_name} "
            f"WHERE {email_column} = :email OR {prn_column} = :prn"
        ),
        {"email": user.email, "prn": user.prn},
    )

    db.session.execute(
        text(
            f"INSERT INTO {table_name} "
            f"({prn_column}, {name_column}, {class_column}, {email_column}, {contact_column}, {department_column}, {year_column}, {password_column}) "
            "VALUES (:prn, :name, :class_name, :email, :contact_number, :department_id, :current_year, :password)"
        ),
        params,
    )


def _sync_role_directory(user, department_id, table_name, role_label):
    columns = _column_lookup(table_name)
    id_column = _pick_column(
        columns,
        "admin_id",
        "teacher_id",
        "placement_cell_id",
        "scholarship_cell_id",
    )
    name_column = _pick_column(columns, "name")
    role_column = _pick_column(columns, "role")
    email_column = _pick_column(columns, "email_id", "email")
    contact_column = _pick_column(columns, "contact_number")
    department_column = _pick_column(columns, "department_id")
    password_column = _pick_optional_column(columns, "password")

    existing = db.session.execute(
        text(
            f"SELECT {id_column} FROM {table_name} WHERE {email_column} = :email LIMIT 1"
        ),
        {"email": user.email},
    ).fetchone()

    params = {
        "name": user.name,
        "role": role_label,
        "email": user.email,
        "contact_number": user.contact_number or "",
        "department_id": department_id,
    }
    if password_column:
        params["password"] = user.password_hash

    if existing:
        update_segments = [
            f"{name_column} = :name",
            f"{role_column} = :role",
            f"{email_column} = :email",
            f"{contact_column} = :contact_number",
            f"{department_column} = :department_id",
        ]
        if password_column:
            update_segments.append(f"{password_column} = :password")
        db.session.execute(
            text(
                f"UPDATE {table_name} SET "
                + ", ".join(update_segments)
                + " "
                f"WHERE {email_column} = :email"
            ),
            params,
        )
        return

    insert_columns = [name_column, role_column, email_column, contact_column, department_column]
    insert_values = [":name", ":role", ":email", ":contact_number", ":department_id"]
    if password_column:
        insert_columns.append(password_column)
        insert_values.append(":password")

    db.session.execute(
        text(
            f"INSERT INTO {table_name} "
            f"({', '.join(insert_columns)}) "
            f"VALUES ({', '.join(insert_values)})"
        ),
        params,
    )


def _get_study_year_label(prn):
    admission_year = _extract_admission_year(prn)
    if admission_year is None:
        return "1st Year BTech"

    current_year = 2026
    year_no = max(1, min(current_year - admission_year, 4))
    labels = {
        1: "1st Year BTech",
        2: "2nd Year BTech",
        3: "3rd Year BTech",
        4: "4th Year BTech",
    }
    return labels[year_no]


def _get_class_label(current_year):
    mapping = {
        "1st Year BTech": "FY",
        "2nd Year BTech": "SY",
        "3rd Year BTech": "TY",
        "4th Year BTech": "BE",
    }
    return mapping.get(current_year, "FY")


def _extract_admission_year(prn):
    if not prn:
        return None

    normalized = str(prn).strip().upper()
    if len(normalized) >= 4 and normalized[:4].isdigit():
        return int(normalized[:4])

    if len(normalized) >= 3 and normalized[1:3].isdigit():
        return 2000 + int(normalized[1:3])

    return None


def _pick_column(columns, *candidates):
    for candidate in candidates:
        if candidate.lower() in columns:
            return columns[candidate.lower()]
    raise KeyError(f"Missing expected column. Tried: {', '.join(candidates)}")


def _pick_optional_column(columns, *candidates):
    for candidate in candidates:
        if candidate.lower() in columns:
            return columns[candidate.lower()]
    return None
