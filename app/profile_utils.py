import base64
import binascii
import re
from pathlib import Path

from flask import current_app, flash, request, session
from werkzeug.utils import secure_filename

from app import db
from app.models import Department, User
from app.workbench_sync import sync_workbench_user

ROLE_EMAIL_PATTERNS = {
    "student": r"^[a-z]+(?:\.[a-z]+)*\d{2}@pccoepune\.org$",
    "teacher": r"^[a-z]+(?:\.[a-z]+)*@pccoepune\.org$",
    "admin": r"^[a-z]+(?:\.[a-z]+)*@pccoepune\.org$",
    "placement": r"^[a-z]+(?:\.[a-z]+)*@pccoepune\.org$",
    "scholarship": r"^[a-z]+(?:\.[a-z]+)*@pccoepune\.org$",
}

IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}


def get_profile_payload(user):
    return {
        "name": user.name,
        "email": user.email,
        "role": user.role.title(),
        "role_key": user.role,
        "contact_number": user.contact_number or "",
        "prn": user.prn or "",
        "department": user.department.name if user.department else "",
        "department_id": user.department_id,
        "department_options": Department.query.order_by(Department.name.asc()).all(),
        "profile_image": build_profile_image_url(user.profile_image),
        "avatar_initials": get_initials(user.name),
    }


def update_user_profile(user):
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    contact_number = request.form.get("contact_number", "").strip()
    prn = request.form.get("prn", "").strip() if user.role == "student" else ""
    department_id = request.form.get("department_id", "").strip()
    profile_image = request.files.get("profile_image")
    cropped_profile_image = request.form.get("profile_image_cropped", "").strip()

    if not name:
        flash("Name is required.", "error")
        return False

    if not email:
        flash("Email is required.", "error")
        return False

    duplicate_user = User.query.filter(User.email == email, User.id != user.id).first()
    if duplicate_user:
        flash("This email is already in use by another account.", "error")
        return False

    if not re.match(ROLE_EMAIL_PATTERNS[user.role], email):
        format_hint = (
            "firstname.lastname24@pccoepune.org"
            if user.role == "student"
            else "firstname.lastname@pccoepune.org"
        )
        flash(
            f"{user.role.title()} email must follow pattern like {format_hint}",
            "error",
        )
        return False

    department = None
    if department_id:
        try:
            department = Department.query.get(int(department_id))
        except ValueError:
            flash("Selected department was not found.", "error")
            return False
        if not department:
            flash("Selected department was not found.", "error")
            return False

    if user.role == "student":
        if not prn:
            flash("PRN is required for student profile.", "error")
            return False
        duplicate_prn = User.query.filter(User.prn == prn, User.id != user.id).first()
        if duplicate_prn:
            flash("This PRN is already assigned to another student.", "error")
            return False
        user.prn = prn

    if cropped_profile_image:
        saved_path = save_cropped_profile_image(cropped_profile_image, user.id)
        if not saved_path:
            return False
        user.profile_image = saved_path
    elif profile_image and profile_image.filename:
        saved_path = save_profile_image(profile_image, user.id)
        if not saved_path:
            return False
        user.profile_image = saved_path

    user.name = name
    user.email = email
    user.contact_number = contact_number or None
    user.department = department

    db.session.flush()
    sync_workbench_user(user)
    db.session.commit()
    session["user"] = {
        "id": user.id,
        "email": user.email,
        "name": user.name,
        "role": user.role,
    }
    flash("Profile updated successfully.", "success")
    return True


def save_profile_image(uploaded_file, user_id):
    extension = (
        uploaded_file.filename.rsplit(".", 1)[-1].lower()
        if "." in uploaded_file.filename
        else ""
    )
    if extension not in IMAGE_EXTENSIONS:
        flash("Profile picture must be PNG, JPG, or JPEG.", "error")
        return None

    file_name = secure_filename(f"profile_{user_id}.{extension}")
    relative_path = Path("profiles") / file_name
    absolute_path = Path(current_app.config["UPLOAD_FOLDER"]) / relative_path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    uploaded_file.save(absolute_path)
    return str(relative_path).replace("\\", "/")


def save_cropped_profile_image(image_data_url, user_id):
    prefix = "data:image/"
    if not image_data_url.startswith(prefix):
        flash("Cropped profile picture format is invalid.", "error")
        return None

    try:
        header, encoded = image_data_url.split(",", 1)
    except ValueError:
        flash("Cropped profile picture data is incomplete.", "error")
        return None

    mime_part = header[len(prefix):].split(";", 1)[0].lower()
    extension = "jpg" if mime_part == "jpeg" else mime_part
    if extension not in IMAGE_EXTENSIONS:
        flash("Profile picture must be PNG, JPG, or JPEG.", "error")
        return None

    try:
        image_bytes = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        flash("Could not read cropped profile picture.", "error")
        return None

    file_name = secure_filename(f"profile_{user_id}.{extension}")
    relative_path = Path("profiles") / file_name
    absolute_path = Path(current_app.config["UPLOAD_FOLDER"]) / relative_path
    absolute_path.parent.mkdir(parents=True, exist_ok=True)
    absolute_path.write_bytes(image_bytes)
    return str(relative_path).replace("\\", "/")


def build_profile_image_url(profile_image):
    if not profile_image:
        return ""
    normalized = str(profile_image).replace("\\", "/")
    if normalized.startswith("http://") or normalized.startswith("https://"):
        return normalized
    upload_root = Path(current_app.config["UPLOAD_FOLDER"]).name
    if normalized.startswith(upload_root + "/"):
        normalized = normalized[len(upload_root) + 1 :]
    return f"/static/uploads/{normalized}"


def get_initials(name):
    parts = [part[0] for part in name.split() if part]
    return "".join(parts[:2]).upper() or "NA"
