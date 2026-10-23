from flask import Blueprint

roadmap_bp = Blueprint("roadmap", __name__)


@roadmap_bp.route("/test")
def test_roadmap():
    return {
        "message": "Roadmap route working"
    }