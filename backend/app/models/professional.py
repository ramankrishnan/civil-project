from datetime import datetime
from decimal import Decimal
from app import db


class ProfessionalProfile(db.Model):
    __tablename__ = "professional_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    profile_photo = db.Column(db.String(500), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    service_description = db.Column(db.Text, nullable=True)
    years_of_experience = db.Column(db.Integer, default=0)
    employment_type = db.Column(db.String(50), default="individual")  # individual, team, freelancer, business
    city = db.Column(db.String(100), nullable=False, index=True)
    locality = db.Column(db.String(150), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True, index=True)
    travel_distance_km = db.Column(db.Integer, default=20)
    pricing_type = db.Column(db.String(30), default="negotiable")  # daily, hourly, per_sqft, per_project, negotiable
    price_amount = db.Column(db.Numeric(12, 2), nullable=True)
    currency = db.Column(db.String(3), default="INR")
    availability = db.Column(db.String(30), default="available", index=True)  # available, busy, temporarily_unavailable
    show_phone_publicly = db.Column(db.Boolean, default=False)
    whatsapp_consent = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False, index=True)
    verification_status = db.Column(db.String(30), default="pending")  # pending, approved, rejected
    profile_visits = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="professional_profile")
    skills = db.relationship("ProfessionalSkill", back_populates="professional", cascade="all, delete-orphan")
    service_areas = db.relationship("ProfessionalServiceArea", back_populates="professional", cascade="all, delete-orphan")
    portfolio_items = db.relationship("PortfolioItem", back_populates="professional", cascade="all, delete-orphan")
    qualifications = db.relationship("Qualification", back_populates="professional", cascade="all, delete-orphan")
    inquiries = db.relationship("ProjectInquiry", back_populates="professional", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="professional", cascade="all, delete-orphan")
    verification_requests = db.relationship("VerificationRequest", back_populates="professional", cascade="all, delete-orphan")

    def average_rating(self):
        if not self.reviews:
            return None
        ratings = [r.rating for r in self.reviews if r.is_approved]
        return round(sum(ratings) / len(ratings), 1) if ratings else None

    def review_count(self):
        return len([r for r in self.reviews if r.is_approved])

    def to_dict(self, include_private=False):
        data = {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "profile_photo": self.profile_photo,
            "introduction": self.introduction,
            "service_description": self.service_description,
            "years_of_experience": self.years_of_experience,
            "employment_type": self.employment_type,
            "city": self.city,
            "locality": self.locality,
            "pin_code": self.pin_code,
            "travel_distance_km": self.travel_distance_km,
            "pricing_type": self.pricing_type,
            "price_amount": float(self.price_amount) if self.price_amount else None,
            "currency": self.currency,
            "availability": self.availability,
            "is_verified": self.is_verified,
            "verification_status": self.verification_status,
            "profile_visits": self.profile_visits,
            "is_active": self.is_active,
            "average_rating": self.average_rating(),
            "review_count": self.review_count(),
            "skills": [s.to_dict() for s in self.skills],
            "portfolio_items": [p.to_dict() for p in self.portfolio_items],
            "qualifications": [q.to_dict() for q in self.qualifications],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_private or self.show_phone_publicly:
            data["phone"] = self.user.phone if self.user else None
        if self.whatsapp_consent and self.user and self.user.phone:
            data["whatsapp"] = self.user.phone
        if include_private:
            data["email"] = self.user.email if self.user else None
            data["show_phone_publicly"] = self.show_phone_publicly
            data["whatsapp_consent"] = self.whatsapp_consent
        return data


class ProfessionalSkill(db.Model):
    __tablename__ = "professional_skills"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("service_categories.id"), nullable=False)
    is_primary = db.Column(db.Boolean, default=False)

    professional = db.relationship("ProfessionalProfile", back_populates="skills")
    category = db.relationship("ServiceCategory")

    def to_dict(self):
        return {
            "id": self.id,
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else None,
            "is_primary": self.is_primary,
        }


class ProfessionalServiceArea(db.Model):
    __tablename__ = "professional_service_areas"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    locality = db.Column(db.String(150), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True)

    professional = db.relationship("ProfessionalProfile", back_populates="service_areas")


class PortfolioItem(db.Model):
    __tablename__ = "portfolio_items"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    professional = db.relationship("ProfessionalProfile", back_populates="portfolio_items")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Qualification(db.Model):
    __tablename__ = "qualifications"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    issuing_body = db.Column(db.String(200), nullable=True)
    year = db.Column(db.Integer, nullable=True)
    document_url = db.Column(db.String(500), nullable=True)  # private – admin only

    professional = db.relationship("ProfessionalProfile", back_populates="qualifications")

    def to_dict(self, include_document=False):
        data = {
            "id": self.id,
            "title": self.title,
            "issuing_body": self.issuing_body,
            "year": self.year,
        }
        if include_document:
            data["document_url"] = self.document_url
        return data
