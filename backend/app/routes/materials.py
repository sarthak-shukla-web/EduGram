from flask import Blueprint

materials_bp = Blueprint("materials", __name__)


@materials_bp.route("/test")
def test_materials():
    return {
        "message": "Materials route working"
    }