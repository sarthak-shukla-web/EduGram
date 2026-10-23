from flask import Blueprint

ai_bp = Blueprint("ai", __name__)


@ai_bp.route("/test")
def test_ai():
    return {
        "message": "AI route working"
    }