from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.models import User
from app.seed import LOGIN_DEMO_USERS
from app.view_models import build_admin_payload

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


@auth_bp.route("/")
def index():
    return render_template("landing/index.html", payload=build_admin_payload())


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

        flash("Invalid email or password. Use one of the preloaded database accounts shown on the page.", "error")

    return render_template("auth/login.html", seeded_users=LOGIN_DEMO_USERS)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    flash("Sign up is disabled. Use the preloaded college login accounts.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.pop("user", None)
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
