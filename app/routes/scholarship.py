from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.profile_utils import get_profile_payload, update_user_profile
from app.session_utils import get_session_user
from app.view_models import build_cell_payload

scholarship_bp = Blueprint("scholarship", __name__, url_prefix="/scholarship")


def scholarship_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "scholarship":
            flash("Scholarship cell access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@scholarship_bp.route("/")
@scholarship_bp.route("/dashboard")
@scholarship_required
def dashboard():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    return render_template("scholarship/dashboard.html", payload=build_cell_payload(user))


@scholarship_bp.route("/profile", methods=["GET", "POST"])
@scholarship_required
def profile():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if update_user_profile(user):
            return redirect(url_for("scholarship.profile"))
    return render_template("scholarship/profile.html", profile=get_profile_payload(user), payload=build_cell_payload(user))
