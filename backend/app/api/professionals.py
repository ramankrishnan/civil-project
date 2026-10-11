from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from sqlalchemy import or_
from app import db
from app.models import (
    User,
    ProfessionalProfile,
    ProfessionalSkill,
    ServiceCategory,
    PortfolioItem,
    SavedProfessional,
    CustomerProfile,
)

professionals_bp = Blueprint("professionals", __name__)


@professionals_bp.route("", methods=["GET"])
def list_professionals():
    """Public search & filter endpoint"""
    page = request.args.get("page", 1, type=int)
    per_page = min(request.args.get("per_page", 12, type=int), 50)
    q = request.args.get("q", "").strip()
    city = request.args.get("city", "").strip()
    locality = request.args.get("locality", "").strip()
    pin_code = request.args.get("pin_code", "").strip()
    category_id = request.args.get("category_id", type=int)
    category_slug = request.args.get("category", "").strip()
    min_experience = request.args.get("min_experience", type=int)
    availability = request.args.get("availability", "").strip()
    verified_only = request.args.get("verified", "").lower() == "true"
    sort = request.args.get("sort", "relevance")  # relevance, experience, rating, newest

    query = ProfessionalProfile.query.filter_by(is_active=True)

    if q:
        query = query.filter(
            or_(
                ProfessionalProfile.full_name.ilike(f"%{q}%"),
                ProfessionalProfile.introduction.ilike(f"%{q}%"),
                ProfessionalProfile.service_description.ilike(f"%{q}%"),
            )
        )
    if city:
        query = query.filter(ProfessionalProfile.city.ilike(f"%{city}%"))
    if locality:
        query = query.filter(ProfessionalProfile.locality.ilike(f"%{locality}%"))
    if pin_code:
        query = query.filter(ProfessionalProfile.pin_code == pin_code)
    if category_id:
        query = query.join(ProfessionalSkill).filter(ProfessionalSkill.category_id == category_id)
    if category_slug:
        query = (
            query.join(ProfessionalSkill)
            .join(ServiceCategory)
            .filter(ServiceCategory.slug == category_slug)
        )
    if min_experience is not None:
        query = query.filter(ProfessionalProfile.years_of_experience >= min_experience)
    if availability:
        query = query.filter(ProfessionalProfile.availability == availability)
    if verified_only:
        query = query.filter(ProfessionalProfile.is_verified == True)

    if sort == "experience":
        query = query.order_by(ProfessionalProfile.years_of_experience.desc())
    elif sort == "newest":
        query = query.order_by(ProfessionalProfile.created_at.desc())
    else:
        query = query.order_by(ProfessionalProfile.is_verified.desc(), ProfessionalProfile.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify(
        {
            "items": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "pages": pagination.pages,
        }
    )


@professionals_bp.route("/<int:prof_id>", methods=["GET"])
def get_professional(prof_id):
    prof = ProfessionalProfile.query.filter_by(id=prof_id, is_active=True).first_or_404()
    # Increment visit count
    prof.profile_visits = (prof.profile_visits or 0) + 1
    db.session.commit()
    return jsonify(prof.to_dict())


@professionals_bp.route("/me", methods=["GET"])
@jwt_required()
def my_profile():
    claims = get_jwt()
    if claims.get("role") != "professional":
        return jsonify({"error": "Only professionals can access this"}), 403
    user_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.filter_by(user_id=user_id).first_or_404()
    return jsonify(prof.to_dict(include_private=True))


@professionals_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    claims = get_jwt()
    if claims.get("role") != "professional":
        return jsonify({"error": "Only professionals can update this"}), 403
    user_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json() or {}

    allowed = [
        "full_name", "introduction", "service_description", "years_of_experience",
        "employment_type", "city", "locality", "pin_code", "travel_distance_km",
        "pricing_type", "price_amount", "availability", "show_phone_publicly",
        "whatsapp_consent", "profile_photo",
    ]
    for field in allowed:
        if field in data:
            setattr(prof, field, data[field])

    # Update skills if provided
    if "skill_ids" in data:
        ProfessionalSkill.query.filter_by(professional_id=prof.id).delete()
        for idx, cat_id in enumerate(data["skill_ids"]):
            skill = ProfessionalSkill(
                professional_id=prof.id,
                category_id=cat_id,
                is_primary=(idx == 0),
            )
            db.session.add(skill)

    db.session.commit()
    return jsonify(prof.to_dict(include_private=True))


@professionals_bp.route("/me/portfolio", methods=["POST"])
@jwt_required()
def add_portfolio():
    claims = get_jwt()
    if claims.get("role") != "professional":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.filter_by(user_id=user_id).first_or_404()
    data = request.get_json() or {}
    if not data.get("image_url"):
        return jsonify({"error": "image_url is required"}), 400
    item = PortfolioItem(
        professional_id=prof.id,
        title=data.get("title"),
        description=data.get("description"),
        image_url=data["image_url"],
    )
    db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@professionals_bp.route("/me/portfolio/<int:item_id>", methods=["DELETE"])
@jwt_required()
def delete_portfolio(item_id):
    claims = get_jwt()
    if claims.get("role") != "professional":
        return jsonify({"error": "Forbidden"}), 403
    user_id = int(get_jwt_identity())
    prof = ProfessionalProfile.query.filter_by(user_id=user_id).first_or_404()
    item = PortfolioItem.query.filter_by(id=item_id, professional_id=prof.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Deleted"})


@professionals_bp.route("/featured", methods=["GET"])
def featured():
    items = (
        ProfessionalProfile.query.filter_by(is_active=True, is_verified=True)
        .order_by(ProfessionalProfile.profile_visits.desc())
        .limit(8)
        .all()
    )
    return jsonify([p.to_dict() for p in items])
