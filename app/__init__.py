from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from dotenv import load_dotenv
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///devlink.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY", "devlink-secret")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")

    # ↓ Comment these until we implement them
    from .routes.projects import projects_bp
    from .routes.admin import admin_bp
    app.register_blueprint(projects_bp, url_prefix="/api/projects")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    return app
