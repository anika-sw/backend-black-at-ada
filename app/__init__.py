from flask import Flask, request, jsonify, make_response, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
import requests

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if not config:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.user import User
    from app.models.event import Event
    from app.models.event_user import EventUser

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    from .user_routes import users_bp
    from .event_routes import events_bp
    from .auth_routes import auth_bp
    from .image_routes import image_bp
    app.register_blueprint(users_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(image_bp)

    CORS(app)
    return app


