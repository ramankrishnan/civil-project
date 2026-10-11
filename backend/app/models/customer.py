from datetime import datetime
from app import db


class CustomerProfile(db.Model):
    __tablename__ = "customer_profiles"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    profile_photo = db.Column(db.String(500), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    locality = db.Column(db.String(150), nullable=True)
    pin_code = db.Column(db.String(10), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = db.relationship("User", back_populates="customer_profile")
    inquiries = db.relationship("ProjectInquiry", back_populates="customer", cascade="all, delete-orphan")
    saved_professionals = db.relationship("SavedProfessional", back_populates="customer", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="customer", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "profile_photo": self.profile_photo,
            "city": self.city,
            "locality": self.locality,
            "pin_code": self.pin_code,
            "email": self.user.email if self.user else None,
            "phone": self.user.phone if self.user else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
