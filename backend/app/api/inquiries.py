from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app import db, limiter
from app.models import (
    ProjectInquiry,
    InquiryStatusHistory,
    CustomerProfile,
    ProfessionalProfile,
    Notification,
    User,
)

inquiries_bp = Blueprint("inquiries", __name__)

VALID_STATUSES = {"new", "contacted", "discussing", "accepted", "completed", "cancelled"}


@inquiries_bp.route("", methods=["POST"])
@jwt_required()
@limiter.limit("30 per hour")
def create_inquiry():
    claims = get_jwt()
    if claims.get("role") != "customer":
        return jsonify({"error": "Only customers can send inquiries"}), 403
    user_id = int(get_jwt_identity())
    customer = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json() or {}

    professional_id = data.get("professional_id")
    work_description = (data.get("work_description") or "").strip()
    if not professional_id or not work_description:
        return jsonify({"error": "professional_id and work_description are required"}), 400

    prof = ProfessionalProfile.query.filter_by(id=professional_id, is_active=True).first_or_404()

    inquiry = ProjectInquiry(
        customer_id=customer.id,
        professional_id=prof.id,
        work_description=work_description,
        location=data.get("location"),
        expected_start_date=data.get("expected_start_date"),
        approximate_budget=data.get("approximate_budget"),
        status="new",
    )
    db.session.add(inquiry)
    db.session.flush()

    history = InquiryStatusHistory(
        inquiry_id=inquiry.id,
        old_status=None,
        new_status="new",
        changed_by_user_id=user_id,
        note="Inquiry created",
    )
    db.session.add(history)

    # Notify professional
    notif = Notification(
        user_id=prof.user_id,
        title="New Project Inquiry",
        message=f"You have a new inquiry from {customer.full_name}",
        type="inquiry",
        link=f"/dashboard/inquiries/{inquiry.id}",
    )
    db.session.add(notif)
    db.session.commit()

    return jsonify(inquiry.to_dict()), 201


@inquiries_bp.route("", methods=["GET"])
@jwt_required()
def list_inquiries():
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    role = claims.get("role")

    if role == "customer":
        profile = CustomerProfile.query.filter_by(user_id=user_id).first_or_404()
        items = ProjectInquiry.query.filter_by(customer_id=profile.id).order_by(ProjectInquiry.created_at.desc()).all()
    elif role == "professional":
        profile = ProfessionalProfile.query.filter_by(user_id=user_id).first_or_404()
        items = ProjectInquiry.query.filter_by(professional_id=profile.id).order_by(ProjectInquiry.created_at.desc()).all()
    else:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify([i.to_dict() for i in items])


@inquiries_bp.route("/<int:inquiry_id>", methods=["GET"])
@jwt_required()
def get_inquiry(inquiry_id):
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    inquiry = ProjectInquiry.query.get_or_404(inquiry_id)

    if claims.get("role") == "customer":
        profile = CustomerProfile.query.filter_by(user_id=user_id).first()
        if not profile or inquiry.customer_id != profile.id:
            return jsonify({"error": "Forbidden"}), 403
    elif claims.get("role") == "professional":
        profile = ProfessionalProfile.query.filter_by(user_id=user_id).first()
        if not profile or inquiry.professional_id != profile.id:
            return jsonify({"error": "Forbidden"}), 403
    else:
        return jsonify({"error": "Forbidden"}), 403

    return jsonify(inquiry.to_dict())


@inquiries_bp.route("/<int:inquiry_id>/status", methods=["PATCH"])
@jwt_required()
def update_status(inquiry_id):
    claims = get_jwt()
    user_id = int(get_jwt_identity())
    inquiry = ProjectInquiry.query.get_or_404(inquiry_id)
    data = request.get_json() or {}
    new_status = data.get("status")
    if new_status not in VALID_STATUSES:
        return jsonify({"error": f"Invalid status. Allowed: {', '.join(VALID_STATUSES)}"}), 400

    # Authorization: customer or professional involved
    allowed = False
    if claims.get("role") == "customer":
        profile = CustomerProfile.query.filter_by(user_id=user_id).first()
        if profile and inquiry.customer_id == profile.id:
            allowed = True
    elif claims.get("role") == "professional":
        profile = ProfessionalProfile.query.filter_by(user_id=user_id).first()
        if profile and inquiry.professional_id == profile.id:
            allowed = True
    if not allowed:
        return jsonify({"error": "Forbidden"}), 403

    old = inquiry.status
    inquiry.status = new_status
    history = InquiryStatusHistory(
        inquiry_id=inquiry.id,
        old_status=old,
        new_status=new_status,
        changed_by_user_id=user_id,
        note=data.get("note"),
    )
    db.session.add(history)
    db.session.commit()
    return jsonify(inquiry.to_dict())
