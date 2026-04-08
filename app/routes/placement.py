from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from app.profile_utils import get_profile_payload, update_user_profile
from app.session_utils import get_session_user
from app.view_models import build_cell_payload

placement_bp = Blueprint("placement", __name__, url_prefix="/placement")


def placement_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        user = session.get("user")
        if not user or user.get("role") != "placement":
            flash("Placement cell access required.", "error")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


@placement_bp.route("/")
@placement_bp.route("/dashboard")
@placement_required
def dashboard():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    return render_template("placement/dashboard.html", payload=build_cell_payload(user))


@placement_bp.route("/profile", methods=["GET", "POST"])
@placement_required
def profile():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        if update_user_profile(user):
            return redirect(url_for("placement.profile"))
    return render_template("placement/profile.html", profile=get_profile_payload(user), payload=build_cell_payload(user))
