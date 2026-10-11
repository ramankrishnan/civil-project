import os
import uuid
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename

uploads_bp = Blueprint("uploads", __name__)

ALLOWED = {"jpg", "jpeg", "png", "webp", "pdf"}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED


@uploads_bp.route("", methods=["POST"])
@jwt_required()
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    if not file or file.filename == "":
        return jsonify({"error": "Empty filename"}), 400
    if not allowed_file(file.filename):
        return jsonify({"error": f"Allowed types: {', '.join(ALLOWED)}"}), 400

    ext = file.filename.rsplit(".", 1)[1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    upload_dir = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(upload_dir, exist_ok=True)
    path = os.path.join(upload_dir, filename)
    file.save(path)

    # In production, upload to Azure Blob and return the public URL
    url = f"/api/uploads/{filename}"
    return jsonify({"url": url, "filename": filename}), 201


@uploads_bp.route("/<path:filename>", methods=["GET"])
def serve_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
