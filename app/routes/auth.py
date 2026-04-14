import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app import db
from app.models import Department, User
from app.seed import LOGIN_DEMO_USERS
from app.view_models import build_admin_payload
from app.workbench_sync import sync_workbench_user

auth_bp = Blueprint("auth", __name__)


def _redirect_by_role(role):
    endpoints = {
        "admin": "admin.dashboard",
        "teacher": "teacher.dashboard",
        "student": "student.dashboard",
        "placement": "placement.dashboard",
        "scholarship": "scholarship.dashboard",
    }
    return redirect(url_for(endpoints.get(role, "auth.login")))


# =========================
# EMAIL PATTERNS (FINAL)
# =========================
ROLE_EMAIL_PATTERNS = {
    "student": r"^[a-z]+\.[a-z]+\.[0-9]{2}@pccoepune\.org$",
    "teacher": r"^[a-z]+\.[a-z]+@pccoepune\.org$",
    "admin": r"^[a-z]+\.[a-z]+@pccoepune\.org$",
    "placement": r"^[a-z]+\.[a-z]+@pccoepune\.org$",
    "scholarship": r"^[a-z]+\.[a-z]+@pccoepune\.org$",
}

ROLE_PASSWORD_PREFIX = {
    "student": "stu-",
    "teacher": "teach-",
    "admin": "admin-",
    "placement": "place-",
    "scholarship": "schol-",
}


@auth_bp.route("/")
def index():
    return render_template("landing/index.html", payload=build_admin_payload())


# =========================
# LOGIN
# =========================
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()

        user = User.query.filter_by(email=email, is_active=True).first()

        if user and user.check_password(password):
            session["user"] = {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            }
            flash(f"Welcome back, {user.name}!", "success")
            return _redirect_by_role(user.role)

        flash("Invalid credentials. Use seeded demo accounts.", "error")

    return render_template("auth/login.html", seeded_users=LOGIN_DEMO_USERS)


# =========================
# REGISTER
# =========================
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        role = request.form.get("role", "").strip().lower()
        department_name = request.form.get("department", "").strip()
        password = request.form.get("password", "").strip()
        contact_number = request.form.get("contact_number", "").strip()
        prn = request.form.get("prn", "").strip() or None

        # -------------------------
        # ROLE VALIDATION
        # -------------------------
        if role not in ROLE_EMAIL_PATTERNS:
            flash("Please choose a valid role.", "error")
            return redirect(url_for("auth.register"))

        # -------------------------
        # EMAIL VALIDATION (FIXED)
        # -------------------------
        pattern = ROLE_EMAIL_PATTERNS[role]

        if not re.match(pattern, email):

            if role == "student":
                msg = "Student email must be firstname.lastname.22@pccoepune.org"
            else:
                msg = "Staff email must be firstname.lastname@pccoepune.org"

            flash(msg, "error")
            return redirect(url_for("auth.register"))

        # -------------------------
        # PASSWORD VALIDATION
        # -------------------------
        if not password.startswith(ROLE_PASSWORD_PREFIX[role]) or len(password) < 8:
            flash(
                f"{role.title()} password must start with {ROLE_PASSWORD_PREFIX[role]}",
                "error",
            )
            return redirect(url_for("auth.register"))

        # -------------------------
        # DUPLICATE EMAIL CHECK
        # -------------------------
        if User.query.filter_by(email=email).first():
            flash("This email is already registered.", "error")
            return redirect(url_for("auth.register"))

        # -------------------------
        # STUDENT PRN CHECK
        # -------------------------
        if role == "student" and not prn:
            flash("PRN is required for student registration.", "error")
            return redirect(url_for("auth.register"))

        if role == "student" and User.query.filter_by(prn=prn).first():
            flash("This PRN is already registered.", "error")
            return redirect(url_for("auth.register"))

        # -------------------------
        # DEPARTMENT HANDLING
        # -------------------------
        department = Department.query.filter_by(name=department_name).first()

        if not department:
            default_departments = {
                "student": ("Computer Engineering", "Academic"),
                "teacher": ("Computer Engineering", "Academic"),
                "admin": ("Administration", "Administrative"),
                "placement": ("Placement Cell", "Placement"),
                "scholarship": ("Scholarship Cell", "Scholarship"),
            }

            resolved_name, resolved_category = default_departments.get(
                role, ("General Department", "Academic")
            )

            department = Department(
                name=department_name or resolved_name,
                category=resolved_category
            )

            db.session.add(department)
            db.session.flush()

        # -------------------------
        # CREATE USER
        # -------------------------
        user = User(
            name=name,
            email=email,
            role=role,
            prn=prn,
            contact_number=contact_number or None,
            department=department,
        )

        user.set_password(password)

        db.session.add(user)
        db.session.flush()

        # external sync
        sync_workbench_user(user)

        db.session.commit()

        flash("Account created successfully. Please sign in.", "success")
        return redirect(url_for("auth.login"))

    # -------------------------
    # GET REQUEST
    # -------------------------
    return render_template(
        "auth/register.html",
        role_examples={
            "student": {
                "email": "firstname.lastname.22@pccoepune.org",
                "password": "stu-2025ce001",
            },
            "teacher": {
                "email": "firstname.lastname@pccoepune.org",
                "password": "teach-meera1",
            },
            "admin": {
                "email": "firstname.lastname@pccoepune.org",
                "password": "admin-aarav1",
            },
            "placement": {
                "email": "firstname.lastname@pccoepune.org",
                "password": "place-kabir1",
            },
            "scholarship": {
                "email": "firstname.lastname@pccoepune.org",
                "password": "schol-neha1",
            },
        },
    )


# =========================
# LOGOUT
# =========================
@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))