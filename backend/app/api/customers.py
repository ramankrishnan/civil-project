from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db
from app.models import CustomerProfile, SavedProfessional, ProfessionalProfile, User

customers_bp = Blueprint("customers", __name__)


@customers_bp.route("/me", methods=["GET"])
@jwt_required()
def my_profile():
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Only customers can access this"}), 403
    user_id = int(get_jwt_identity())
    profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    return jsonify(profile.to_dict())


@customers_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json() or {}
    for field in ["full_name", "city", "locality", "pin_code", "profile_photo"]:
        if field in data:
            setattr(profile, field, data[field])
    db.session.commit()
    return jsonify(profile.to_dict())


@customers_bp.route("/saved", methods=["GET"])
@jwt_required()
def list_saved():
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    saved = SavedProfessional.query.filter_by(customer_id=profile.id).all()
    return jsonify([s.professional.to_dict() for s in saved if s.professional and s.professional.is_active])


@customers_bp.route("/saved/<int:prof_id>", methods=["POST"])
@jwt_required()
def save_professional(prof_id):
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    ProfessionalProfile.query.filter_by(id=prof_id, is_active=True).first_or_404()
    existing = SavedProfessional.query.filter_by(customer_id=profile.id, professional_id=prof_id).first()
    if existing:
        return jsonify({"message": "Already saved"}), 200
    saved = SavedProfessional(customer_id=profile.id, professional_id=prof_id)
    db.session.add(saved)
    db.session.commit()
    return jsonify({"message": "Saved"}), 201


@customers_bp.route("/saved/<int:prof_id>", methods=["DELETE"])
@jwt_required()
def unsave_professional(prof_id):
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    saved = SavedProfessional.query.filter_by(customer_id=profile.id, professional_id=prof_id).first_or_404()
    db.session.delete(saved)
    db.session.commit()
    return jsonify({"message": "Removed"})
