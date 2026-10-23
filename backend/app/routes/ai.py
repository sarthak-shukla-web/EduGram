import os
import tempfile
from pathlib import Path

from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename

from app.services.document_analyzer import (
    analyze_document,
    DocumentAnalysisError,
)
from app.services.pdf_processor import PDFProcessingError
from app.services.ai_engine import AIEngineError


ai_bp = Blueprint("ai", __name__)

MAX_UPLOAD_SIZE = 15 * 1024 * 1024  # 15 MB
ALLOWED_EXTENSION = ".pdf"


@ai_bp.route("/test", methods=["GET"])
def test_ai():
    return jsonify({
        "success": True,
        "message": "AI route working"
    }), 200


@ai_bp.route("/analyze", methods=["POST"])
def analyze_pdf():
    """
    Accept a PDF upload and return its summary, topics,
    and recommended learning path.
    """

    # 1. Check whether a file was included.
    if "file" not in request.files:
        return jsonify({
            "success": False,
            "error": "No file was uploaded. Use the 'file' field."
        }), 400

    uploaded_file = request.files["file"]

    # 2. Check whether a filename was supplied.
    if not uploaded_file.filename:
        return jsonify({
            "success": False,
            "error": "No file was selected."
        }), 400

    # 3. Sanitize the filename.
    filename = secure_filename(uploaded_file.filename)

    if not filename:
        return jsonify({
            "success": False,
            "error": "Invalid filename."
        }), 400

    # 4. Only accept PDFs.
    if Path(filename).suffix.lower() != ALLOWED_EXTENSION:
        return jsonify({
            "success": False,
            "error": "Only PDF files are supported."
        }), 415

    # 5. Read the upload and enforce the size limit.
    # Reading at most one byte over the limit prevents an
    # unrestricted read into memory.
    file_bytes = uploaded_file.stream.read(MAX_UPLOAD_SIZE + 1)

    if not file_bytes:
        return jsonify({
            "success": False,
            "error": "The uploaded file is empty."
        }), 400

    if len(file_bytes) > MAX_UPLOAD_SIZE:
        return jsonify({
            "success": False,
            "error": "The PDF exceeds the 15 MB limit."
        }), 413

    # 6. Save temporarily, process, and always clean up.
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            mode="wb",
            suffix=".pdf",
            delete=False
        ) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name

        result = analyze_document(temp_path)

        # Return the original sanitized filename rather than
        # the randomly generated temporary filename.
        result["filename"] = filename

        return jsonify({
            "success": True,
            "data": result
        }), 200

    except PDFProcessingError as exc:
        return jsonify({
            "success": False,
            "error": str(exc)
        }), 400

    except (AIEngineError, DocumentAnalysisError):
        return jsonify({
            "success": False,
            "error": (
                "Document analysis failed. "
                "Please try again with a readable PDF."
            )
        }), 500

    except Exception:
        # Avoid exposing internal exception details to clients.
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred during analysis."
        }), 500

    finally:
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass