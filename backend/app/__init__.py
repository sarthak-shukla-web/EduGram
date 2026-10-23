from flask import Flask
from flask_cors import CORS

from .config import Config
from .extensions import db, jwt

from .models import (
    User,
    Material,
    Topic,
    Roadmap,
    RoadmapTopic,
    Progress
)

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": "http://localhost:5173"
            }
        }
    )

    db.init_app(app)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.materials import materials_bp
    from .routes.roadmap import roadmap_bp
    from .routes.progress import progress_bp
    from .routes.ai import ai_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(materials_bp, url_prefix="/api/materials")
    app.register_blueprint(roadmap_bp, url_prefix="/api/roadmap")
    app.register_blueprint(progress_bp, url_prefix="/api/progress")
    app.register_blueprint(ai_bp, url_prefix="/api/ai")

    @app.route("/api/health")
    def health():
        return {
            "status": "success",
            "message": "EduGram backend is running!"
        }

    with app.app_context():
        db.create_all()

    return app