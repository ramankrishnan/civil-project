import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])


def create_app(config_name=None):
    app = Flask(__name__)

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-me")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "postgresql://nirman:nirmanpass@localhost:5432/nirmanconnect"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 2592000  # 30 days
    app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_CONTENT_LENGTH", 10 * 1024 * 1024))
    app.config["UPLOAD_FOLDER"] = os.getenv("UPLOAD_FOLDER", "uploads")
    app.config["FRONTEND_URL"] = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Ensure upload folder exists
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)

    CORS(
        app,
        origins=[app.config["FRONTEND_URL"], "http://localhost:5173", "http://127.0.0.1:5173"],
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
    )

    # Register blueprints
    from app.api.auth import auth_bp
    from app.api.professionals import professionals_bp
    from app.api.customers import customers_bp
    from app.api.inquiries import inquiries_bp
    from app.api.admin import admin_bp
    from app.api.categories import categories_bp
    from app.api.uploads import uploads_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(professionals_bp, url_prefix="/api/professionals")
    app.register_blueprint(customers_bp, url_prefix="/api/customers")
    app.register_blueprint(inquiries_bp, url_prefix="/api/inquiries")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(uploads_bp, url_prefix="/api/uploads")

    @app.route("/api/health")
    def health():
        return {"status": "ok", "service": "NirmanConnect API"}

    return app
