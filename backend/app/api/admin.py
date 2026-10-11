from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from functools import wraps
from app import db
from app.models import (
    User,
    ProfessionalProfile,
    CustomerProfile,
    VerificationRequest,
    Report,
    AdminAuditLog,
    ServiceCategory,
    ProjectInquiry,
)

admin_bp = Blueprint("admin", __name__)


def admin_required(fn):
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        claims = get_jwt()
        if claims.get("role") != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper


def log_action(admin_id, action, target_type=None, target_id=None, details=None):
    entry = AdminAuditLog(
        admin_id=admin_id,
        action=action,
        target_type=target_type,
        target_id=target_id,
        details=details,
    )
    db.session.add(entry)


@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    return jsonify(
        {
            "total_users": User.query.count(),
            "total_customers": User.query.filter_by(role="customer").count(),
            "total_professionals": User.query.filter_by(role="professional").count(),
            "active_professionals": ProfessionalProfile.query.filter_by(is_active=True).count(),
            "pending_verifications": VerificationRequest.query.filter_by(status="pending").count(),
            "pending_reports": Report.query.filter_by(status="pending").count(),
            "total_inquiries": ProjectInquiry.query.count(),
        }
    )


@admin_bp.route("/professionals", methods=["GET"])
@admin_required
def list_professionals():
    page = request.args.get("page", 1, type=int)
    status = request.args.get("status")  # active, inactive, pending_verification
    query = ProfessionalProfile.query
    if status == "active":
        query = query.filter_by(is_active=True)
    elif status == "inactive":
        query = query.filter_by(is_active=False)
    pagination = query.order_by(ProfessionalProfile.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify(
        {
            "items": [p.to_dict(include_private=True) for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


@admin_bp.route("/professionals/<int:prof_id>/verify", methods=["POST"])
@admin_required
def verify_professional(prof_id):
    admin_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.get_or_404(prof_id)
    data = request.get_json() or {}
    action = data.get("action", "approve")  # approve / reject

    if action == "approve":
        prof.is_verified = True
        prof.verification_status = "approved"
    else:
        prof.is_verified = False
        prof.verification_status = "rejected"

    log_action(admin_id, f"verification_{action}", "professional", prof_id, data.get("note"))
    db.session.commit()
    return jsonify(prof.to_dict(include_private=True))


@admin_bp.route("/professionals/<int:prof_id>/suspend", methods=["POST"])
@admin_required
def suspend_professional(prof_id):
    admin_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.get_or_404(prof_id)
    prof.is_active = False
    if prof.user:
        prof.user.is_active = False
    log_action(admin_id, "suspend_professional", "professional", prof_id)
    db.session.commit()
    return jsonify({"message": "Professional suspended"})


@admin_bp.route("/professionals/<int:prof_id>/activate", methods=["POST"])
@admin_required
def activate_professional(prof_id):
    admin_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.get_or_404(prof_id)
    prof.is_active = True
    if prof.user:
        prof.user.is_active = True
    log_action(admin_id, "activate_professional", "professional", prof_id)
    db.session.commit()
    return jsonify({"message": "Professional activated"})


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    page = request.args.get("page", 1, type=int)
    role = request.args.get("role")
    query = User.query
    if role:
        query = query.filter_by(role=role)
    pagination = query.order_by(User.created_at.desc()).paginate(page=page, per_page=20, error_out=False)
    return jsonify(
        {
            "items": [u.to_dict() for u in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


@admin_bp.route("/reports", methods=["GET"])
@admin_required
def list_reports():
    status = request.args.get("status", "pending")
    items = Report.query.filter_by(status=status).order_by(Report.created_at.desc()).limit(50).all()
    return jsonify(
        [
            {
                "id": r.id,
                "reason": r.reason,
                "description": r.description,
                "status": r.status,
                "reporter_id": r.reporter_id,
                "reported_user_id": r.reported_user_id,
                "created_at": r.created_at.isoformat() if r.created_at else None,
            }
            for r in items
        ]
    )


@admin_bp.route("/categories", methods=["POST"])
@admin_required
def create_category():
    admin_id = int(get_jwt_identity())
    data = request.get_json() or {}
    name = (data.get("name") or "").strip()
    if not name:
        return jsonify({"error": "name is required"}), 400
    slug = name.lower().replace(" ", "-")
    if ServiceCategory.query.filter_by(slug=slug).first():
        return jsonify({"error": "Category already exists"}), 409
    cat = ServiceCategory(
        name=name,
        slug=slug,
        description=data.get("description"),
        icon=data.get("icon"),
        sort_order=data.get("sort_order", 0),
    )
    db.session.add(cat)
    log_action(admin_id, "create_category", "category", None, name)
    db.session.commit()
    return jsonify(cat.to_dict()), 201


@admin_bp.route("/audit-logs", methods=["GET"])
@admin_required
def audit_logs():
    items = AdminAuditLog.query.order_by(AdminAuditLog.created_at.desc()).limit(100).all()
    return jsonify(
        [
            {
                "id": a.id,
                "admin_id": a.admin_id,
                "action": a.action,
                "target_type": a.target_type,
                "target_id": a.target_id,
                "details": a.details,
                "created_at": a.created_at.isoformat() if a.created_at else None,
            }
            for a in items
        ]
    )
