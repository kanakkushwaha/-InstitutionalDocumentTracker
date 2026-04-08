from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.profile_utils import get_profile_payload, update_user_profile
from app.session_utils import get_session_user
from app.view_models import build_student_dashboard

student_bp = Blueprint("student", __name__, url_prefix="/student")


def student_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "student":
            flash("Student access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@student_bp.route("/dashboard")
@student_required
def dashboard():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    return render_template("student/dashboard.html", payload=build_student_dashboard(user))


@student_bp.route("/profile", methods=["GET", "POST"])
@student_required
def profile():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if update_user_profile(user):
            return redirect(url_for("student.profile"))
    payload = build_student_dashboard(user)
    return render_template("student/profile.html", payload=payload, profile=get_profile_payload(user))


@student_bp.route("/upload")
@student_required
def upload_docs():
    flash("Use the upload control directly inside the document table.", "success")
    return redirect(url_for("student.dashboard"))


@student_bp.route("/documents")
@student_required
def my_documents():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    payload = build_student_dashboard(user)
    return render_template("student/my_documents.html", payload=payload, documents=payload["documents"])
