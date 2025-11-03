from __future__ import annotations

import os
from typing import Dict

from flask import Flask, redirect, render_template, url_for
from flask_login import current_user
from flask.cli import with_appcontext

from .extensions import csrf, db, login_manager, migrate
from .models import Gift, Purchase, User

CONFIG_MAPPING: Dict[str, str] = {
    "development": "config.DevelopmentConfig",
    "production": "config.ProductionConfig",
    "testing": "config.TestingConfig",
}


def create_app(config_name: str | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=False)

    if not config_name:
        config_name = os.getenv("FLASK_ENV", "development")
    config_path = CONFIG_MAPPING.get(config_name, config_name)
    app.config.from_object(config_path)

    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    register_cli(app)
    initialize_database(app)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("gifts.dashboard"))
        return render_template("index.html")

    return app


def register_extensions(app: Flask) -> None:
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"


def register_blueprints(app: Flask) -> None:
    from .auth.routes import auth_bp
    from .gifts.routes import gifts_bp
    from .purchases.routes import purchases_bp
    from .users.routes import users_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(gifts_bp)
    app.register_blueprint(purchases_bp)
    app.register_blueprint(users_bp)


def register_shellcontext(app: Flask) -> None:
    @app.shell_context_processor
    def shell_context():
        return {"db": db, "User": User, "Gift": Gift, "Purchase": Purchase}


def register_cli(app: Flask) -> None:
    from .services.seed import seed_demo_data

    @app.cli.command("seed")
    @with_appcontext
    def seed() -> None:
        seed_demo_data()


def initialize_database(app: Flask) -> None:
    """Ensure that the database schema exists before handling requests."""

    with app.app_context():
        db.create_all()


__all__ = ["create_app", "db"]
