from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt,
)
from app import db, limiter
from app.models import User, CustomerProfile, ProfessionalProfile

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
@limiter.limit("10 per hour")
def register():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = data.get("role", "customer")
    full_name = (data.get("full_name") or "").strip()
    phone = (data.get("phone") or "").strip() or None

    if role not in ("customer", "professional"):
        return jsonify({"error": "Invalid role. Use customer or professional."}), 400
    if not email or not password or not full_name:
        return jsonify({"error": "email, password and full_name are required"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409
    if phone and User.query.filter_by(phone=phone).first():
        return jsonify({"error": "Phone number already registered"}), 409

    user = User(email=email, phone=phone, role=role)
    user.set_password(password)
    db.session.add(user)
    db.session.flush()

    if role == "customer":
        profile = CustomerProfile(
            user_id=user.id,
            full_name=full_name,
            city=data.get("city"),
            locality=data.get("locality"),
            pin_code=data.get("pin_code"),
        )
        db.session.add(profile)
    else:
        city = (data.get("city") or "").strip()
        if not city:
            return jsonify({"error": "City is required for professionals"}), 400
        profile = ProfessionalProfile(
            user_id=user.id,
            full_name=full_name,
            city=city,
            locality=data.get("locality"),
            pin_code=data.get("pin_code"),
            years_of_experience=int(data.get("years_of_experience") or 0),
            introduction=data.get("introduction"),
        )
        db.session.add(profile)

    db.session.commit()

    access = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh = create_refresh_token(identity=str(user.id))

    return (
        jsonify(
            {
                "message": "Registration successful",
                "access_token": access,
                "refresh_token": refresh,
                "user": user.to_dict(),
            }
        ),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
@limiter.limit("20 per hour")
def login():
    data = request.get_json() or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401
    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    user.last_login = datetime.utcnow()
    db.session.commit()

    access = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh = create_refresh_token(identity=str(user.id))

    return jsonify(
        {
            "access_token": access,
            "refresh_token": refresh,
            "user": user.to_dict(),
        }
    )


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    access = create_access_token(identity=identity, additional_claims={"role": claims.get("role")})
    return jsonify({"access_token": access})


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = user.to_dict()
    if user.role == "customer" and user.customer_profile:
        data["profile"] = user.customer_profile.to_dict()
    elif user.role == "professional" and user.professional_profile:
        data["profile"] = user.professional_profile.to_dict(include_private=True)
    return jsonify(data)


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Client should discard tokens. Server-side blacklist can be added later.
    return jsonify({"message": "Logged out successfully"})
