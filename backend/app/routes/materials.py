import os
from flask import Blueprint, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from ..extensions import db
from ..models.material import Material


materials_bp = Blueprint("materials", __name__)

ALLOWED_EXTENSIONS = {"pdf"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@materials_bp.route("/test", methods=["GET"])
def test_materials():
    return {
        "message": "Materials route working"
    }


@materials_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_material():

    user_id = get_jwt_identity()

    if "file" not in request.files:
        return {
            "status": "error",
            "message": "No file provided"
        }, 400

    file = request.files["file"]

    if not file or file.filename == "":
        return {
            "status": "error",
            "message": "No file selected"
        }, 400

    if not allowed_file(file.filename):
        return {
            "status": "error",
            "message": "Only PDF files are allowed"
        }, 400

    original_filename = secure_filename(file.filename)

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    user_folder = os.path.join(
        upload_folder,
        str(user_id)
    )

    os.makedirs(user_folder, exist_ok=True)

    file_path = os.path.join(
        user_folder,
        original_filename
    )

    file.save(file_path)

    material = Material(
        user_id=int(user_id),
        filename=original_filename,
        file_type="pdf",
        file_path=file_path,
        processing_status="pending"
    )

    db.session.add(material)
    db.session.commit()

    return {
        "status": "success",
        "message": "Material uploaded successfully",
        "material": material.to_dict()
    }, 201


@materials_bp.route("", methods=["GET"])
@jwt_required()
def get_materials():

    user_id = get_jwt_identity()

    materials = Material.query.filter_by(
        user_id=int(user_id)
    ).order_by(
        Material.uploaded_at.desc()
    ).all()

    return {
        "status": "success",
        "materials": [
            material.to_dict()
            for material in materials
        ]
    }, 200


@materials_bp.route("/<int:material_id>", methods=["GET"])
@jwt_required()
def get_material(material_id):

    user_id = get_jwt_identity()

    material = Material.query.filter_by(
        id=material_id,
        user_id=int(user_id)
    ).first()

    if not material:
        return {
            "status": "error",
            "message": "Material not found"
        }, 404

    return {
        "status": "success",
        "material": material.to_dict()
    }, 200


@materials_bp.route("/<int:material_id>", methods=["DELETE"])
@jwt_required()
def delete_material(material_id):

    user_id = get_jwt_identity()

    material = Material.query.filter_by(
        id=material_id,
        user_id=int(user_id)
    ).first()

    if not material:
        return {
            "status": "error",
            "message": "Material not found"
        }, 404

    if os.path.exists(material.file_path):
        os.remove(material.file_path)

    db.session.delete(material)
    db.session.commit()

    return {
        "status": "success",
        "message": "Material deleted successfully"
    }, 200