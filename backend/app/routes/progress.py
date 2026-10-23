from flask import Blueprint

progress_bp = Blueprint("progress", __name__)


@progress_bp.route("/test")
def test_progress():
    return {
        "message": "Progress route working"
    }