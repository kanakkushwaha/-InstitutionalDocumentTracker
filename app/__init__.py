from pathlib import Path

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)

    from app.routes import register_blueprints

    register_blueprints(app)

    with app.app_context():
        from app import models
        from app.seed import ensure_seed_data

        app.jinja_env.globals["app_name"] = "Institutional Document Tracker"
        app.jinja_env.globals["current_year"] = 2026
        ensure_seed_data(app)

    return app
