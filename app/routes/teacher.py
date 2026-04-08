from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.profile_utils import get_profile_payload, update_user_profile
from app.session_utils import get_session_user
from app.view_models import build_teacher_payload

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


def teacher_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "teacher":
            flash("Teacher access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@teacher_bp.route("/dashboard")
@teacher_required
def dashboard():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    return render_template("teacher/dashboard.html", payload=build_teacher_payload(user))


@teacher_bp.route("/profile", methods=["GET", "POST"])
@teacher_required
def profile():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if update_user_profile(user):
            return redirect(url_for("teacher.profile"))
    return render_template("teacher/profile.html", teacher=user, profile=get_profile_payload(user))


@teacher_bp.route("/students")
@teacher_required
def students():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    return render_template("teacher/students.html", students=build_teacher_payload(user)["students"])


@teacher_bp.route("/documents")
@teacher_required
def documents():
    return redirect(url_for("teacher.dashboard"))
