import mimetypes
from io import BytesIO
from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, send_file, url_for
from werkzeug.utils import secure_filename

from app import db
from app.models import Department, Document, User
from app.session_utils import get_session_user
from app.view_models import (
    TEACHER_DOCUMENT_CATALOG,
    build_student_dashboard,
    build_student_document_catalog,
    serialize_document,
)

documents_bp = Blueprint("documents", __name__, url_prefix="/documents")


@documents_bp.route("/")
def list_documents():
    category = request.args.get("category")
    documents_query = Document.query.order_by(Document.created_at.desc())
    if category:
        documents_query = documents_query.filter(Document.category.ilike(category))
    documents = [serialize_document(doc) for doc in documents_query.all()]
    user = User.query.filter_by(role="student").order_by(User.id.asc()).first()
    payload = build_student_dashboard(user) if user else {"documents": documents, "student": {}, "notification": ""}
    return render_template("student/my_documents.html", documents=documents, payload=payload)


@documents_bp.route("/upload", methods=["POST"])
def upload_document():
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))

    preset_key = request.form.get("preset_key", "").strip()
    catalog = build_student_document_catalog(user) if user.role == "student" else TEACHER_DOCUMENT_CATALOG
    selected_preset = next((item for item in catalog if item["key"] == preset_key), None)
    uploaded_file = request.files.get("file")
    link_value = request.form.get("link_value", "").strip()

    if not selected_preset:
        flash("Invalid document preset selected.", "error")
        return redirect(url_for("student.dashboard"))

    input_kind = selected_preset.get("input_kind", "file")

    document = Document.query.filter_by(owner_id=user.id, title=selected_preset["name"]).first()
    if not document:
        department = User.query.get(user.id).department
        if selected_preset["department"] != (department.name if department else ""):
            department = Department.query.filter_by(name=selected_preset["department"]).first() or department
        document = Document(
            title=selected_preset["name"],
            category=selected_preset["category"],
            owner_id=user.id,
            department=department,
        )
        db.session.add(document)

    if input_kind == "link":
        if not link_value:
            flash("Please enter the link before saving.", "error")
            return redirect(url_for("student.dashboard"))
        if not (link_value.startswith("http://") or link_value.startswith("https://")):
            flash("Link must start with http:// or https://", "error")
            return redirect(url_for("student.dashboard"))
        document.file_name = selected_preset["name"]
        document.file_type = "LINK"
        document.file_path = link_value
    else:
        if not uploaded_file or not uploaded_file.filename:
            flash("Please choose a file before uploading.", "error")
            return redirect(url_for("student.dashboard"))

        extension = uploaded_file.filename.rsplit(".", 1)[-1].lower() if "." in uploaded_file.filename else ""
        if extension not in current_app.config["ALLOWED_EXTENSIONS"]:
            flash("Unsupported file type.", "error")
            return redirect(url_for("student.dashboard"))

        safe_name = secure_filename(f"{user.id}_{preset_key}.{extension}")
        upload_path = Path(current_app.config["UPLOAD_FOLDER"]) / safe_name
        upload_path.parent.mkdir(parents=True, exist_ok=True)
        uploaded_file.save(upload_path)

        document.file_name = safe_name
        document.file_type = extension.upper()
        document.file_path = str(upload_path)

    document.description = selected_preset["about"]
    document.status = "Pending"
    document.remarks = "Uploaded from preset student document table."
    db.session.commit()

    flash(f"{selected_preset['name']} uploaded successfully.", "success")
    if user.role == "teacher":
        return redirect(url_for("teacher.dashboard"))
    if user.role == "placement":
        return redirect(url_for("placement.dashboard"))
    if user.role == "scholarship":
        return redirect(url_for("scholarship.dashboard"))
    return redirect(url_for("student.dashboard"))


@documents_bp.route("/<doc_id>/review", methods=["POST"])
def review_document(doc_id):
    reviewer = get_session_user()
    if not reviewer or reviewer.role not in {"teacher", "admin", "placement", "scholarship"}:
        flash("Only teacher, admin, placement cell, or scholarship cell can review documents.", "error")
        return redirect(url_for("auth.login"))

    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    status = request.form.get("status", "").strip() or "Pending"
    message = request.form.get("message", "").strip()
    valid_statuses = {"Approved", "Pending", "Changes Requested", "Rejected"}
    if status not in valid_statuses:
        status = "Pending"

    document.status = status
    if message:
        document.remarks = f"{reviewer.name} ({reviewer.role.title()}) asked: {message}"
    else:
        document.remarks = f"Reviewed by {reviewer.name} ({reviewer.role.title()})."
    db.session.commit()
    flash("Review saved successfully.", "success")

    if reviewer.role == "admin":
        return redirect(url_for("admin.manage_documents"))
    if reviewer.role == "placement":
        return redirect(url_for("placement.dashboard"))
    if reviewer.role == "scholarship":
        return redirect(url_for("scholarship.dashboard"))
    return redirect(url_for("teacher.dashboard"))


@documents_bp.route("/<doc_id>")
def view_document(doc_id):
    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    user = get_session_user()
    if not document:
        abort(404)
    serialized = _serialize_document_for_actions(document)
    return render_template(
        "documents/view.html",
        document=serialized,
        can_manage=_can_manage_document(document, user),
        return_endpoint=_get_return_endpoint(user),
        inline_preview_url=_build_inline_preview_url(document),
        preview_mode=_get_preview_mode(document),
    )


@documents_bp.route("/<doc_id>/preview")
def preview_document(doc_id):
    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    user = get_session_user()
    if not document:
        abort(404)
    serialized = _serialize_document_for_actions(document)
    return render_template(
        "documents/preview.html",
        document=serialized,
        can_manage=_can_manage_document(document, user),
        return_endpoint=_get_return_endpoint(user),
        inline_preview_url=_build_inline_preview_url(document),
        preview_mode=_get_preview_mode(document),
    )


@documents_bp.route("/<doc_id>/file")
def inline_document_file(doc_id):
    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    if not document:
        abort(404)
    if (document.file_type or "").upper() == "LINK" and document.file_path:
        return redirect(document.file_path)

    file_path = Path(document.file_path) if document.file_path else None
    if not file_path or not file_path.exists():
        abort(404)

    mime_type = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    return send_file(file_path, as_attachment=False, download_name=document.file_name, mimetype=mime_type)


@documents_bp.route("/<doc_id>/download")
def download_document(doc_id):
    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    if not document:
        abort(404)
    serialized = serialize_document(document)
    if (document.file_type or "").upper() == "LINK" and document.file_path:
        return redirect(document.file_path)
    file_path = Path(document.file_path) if document.file_path else None

    if file_path and file_path.exists():
        return send_file(file_path, as_attachment=True, download_name=document.file_name)

    content = (
        f"{serialized['name']}\n"
        f"Owner: {serialized['owner']}\n"
        f"Department: {serialized['department']}\n"
        f"About: {serialized['about']}\n"
    ).encode("utf-8")

    return send_file(BytesIO(content), as_attachment=True, download_name=document.file_name, mimetype="application/octet-stream")


@documents_bp.route("/<doc_id>/delete", methods=["POST"])
def delete_document(doc_id):
    user = get_session_user()
    if not user:
        flash("Please login again.", "error")
        return redirect(url_for("auth.login"))

    document = Document.query.get_or_404(_normalize_doc_id(doc_id))
    if not _can_manage_document(document, user):
        flash("You are not allowed to delete this document.", "error")
        return redirect(url_for("documents.preview_document", doc_id=document.id))

    file_path = Path(document.file_path) if document.file_path else None
    if file_path and file_path.exists() and _is_within_upload_folder(file_path):
        file_path.unlink(missing_ok=True)

    title = document.title
    db.session.delete(document)
    db.session.commit()

    flash(f"{title} deleted successfully.", "success")
    return redirect(url_for(_get_return_endpoint(user)))


def _normalize_doc_id(doc_id):
    return int(str(doc_id).replace("DOC-", ""))


def _serialize_document_for_actions(document):
    serialized = serialize_document(document)
    catalog = (
        build_student_document_catalog(document.owner)
        if document.owner and document.owner.role == "student"
        else TEACHER_DOCUMENT_CATALOG
    )
    preset = next((item for item in catalog if item["name"] == document.title), None)
    serialized["preset_key"] = preset["key"] if preset else ""
    return serialized


def _get_preview_mode(document):
    file_type = (document.file_type or "").upper()
    if file_type == "PDF":
        return "pdf"
    if file_type in {"PNG", "JPG", "JPEG"}:
        return "image"
    if file_type == "LINK":
        return "link"
    return "unsupported"


def _build_inline_preview_url(document):
    preview_mode = _get_preview_mode(document)
    if preview_mode == "link":
        return document.file_path
    if preview_mode in {"pdf", "image"}:
        return url_for("documents.inline_document_file", doc_id=document.id)
    return None


def _get_return_endpoint(user):
    if not user:
        return "auth.login"
    if user.role == "teacher":
        return "teacher.dashboard"
    if user.role == "admin":
        return "admin.manage_documents"
    if user.role == "placement":
        return "placement.dashboard"
    if user.role == "scholarship":
        return "scholarship.dashboard"
    return "student.dashboard"


def _can_manage_document(document, user):
    if not user:
        return False
    return document.owner_id == user.id


def _is_within_upload_folder(file_path):
    upload_root = Path(current_app.config["UPLOAD_FOLDER"]).resolve()
    try:
        file_path.resolve().relative_to(upload_root)
        return True
    except ValueError:
        return False
