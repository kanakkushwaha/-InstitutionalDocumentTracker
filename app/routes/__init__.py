from .admin import admin_bp
from .auth import auth_bp
from .documents import documents_bp
from .placement import placement_bp
from .scholarship import scholarship_bp
from .student import student_bp
from .teacher import teacher_bp


def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(documents_bp)
    app.register_blueprint(placement_bp)
    app.register_blueprint(scholarship_bp)
