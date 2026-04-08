from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.profile_utils import get_profile_payload, update_user_profile
from app.session_utils import get_session_user
from app.view_models import build_admin_payload, group_users

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "admin":
            flash("Admin access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    payload = build_admin_payload()
    payload["users"] = group_users(payload["users"])
    return render_template("admin/dashboard.html", payload=payload)


@admin_bp.route("/profile", methods=["GET", "POST"])
@admin_required
def profile():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if update_user_profile(user):
            return redirect(url_for("admin.profile"))
    return render_template("admin/profile.html", profile=get_profile_payload(user))


@admin_bp.route("/users")
@admin_required
def manage_users():
    payload = build_admin_payload()
    return render_template("admin/manage_users.html", users=group_users(payload["users"]))


@admin_bp.route("/documents")
@admin_required
def manage_documents():
    payload = build_admin_payload()
    payload["users"] = group_users(payload["users"])
    return render_template("admin/manage_docs.html", payload=payload)


@admin_bp.route("/departments")
@admin_required
def departments():
    payload = build_admin_payload()
    payload["users"] = group_users(payload["users"])
    return render_template("admin/departments.html", payload=payload)


@admin_bp.route("/reports")
@admin_required
def reports():
    payload = build_admin_payload()
    payload["users"] = group_users(payload["users"])
    return render_template("admin/reports.html", payload=payload)
