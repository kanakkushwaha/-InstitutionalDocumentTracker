from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from app import db


# =========================
# TIMESTAMP MIXIN
# =========================
class TimestampMixin:
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


# =========================
# DEPARTMENT MODEL
# =========================
class Department(TimestampMixin, db.Model):
    __tablename__ = "departments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    category = db.Column(db.String(80), nullable=False, default="Academic")
    contact_email = db.Column(db.String(120))
    contact_number = db.Column(db.String(20))

    users = db.relationship(
        "User",
        back_populates="department",
        cascade="all, delete",
        lazy=True
    )

    documents = db.relationship(
        "Document",
        back_populates="department",
        cascade="all, delete",
        lazy=True
    )


# =========================
# USER MODEL
# =========================
class User(TimestampMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(30), nullable=False)

    prn = db.Column(db.String(30), unique=True)
    contact_number = db.Column(db.String(20))
    profile_image = db.Column(db.String(255))

    is_active = db.Column(db.Boolean, default=True, nullable=False)

    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    department = db.relationship("Department", back_populates="users")

    documents = db.relationship(
        "Document",
        back_populates="owner",
        cascade="all, delete",
        lazy=True
    )

    # =========================
    # PASSWORD HANDLING (FIXED)
    # =========================
    def set_password(self, password):
        self.password_hash = generate_password_hash(
            password,
            method="pbkdf2:sha256"
        )

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)


# =========================
# DOCUMENT MODEL
# =========================
class Document(TimestampMixin, db.Model):
    __tablename__ = "documents"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)

    file_name = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(20))
    file_path = db.Column(db.String(255))

    description = db.Column(db.Text)

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    remarks = db.Column(db.Text)

    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey("departments.id"))

    owner = db.relationship("User", back_populates="documents")
    department = db.relationship("Department", back_populates="documents")