from datetime import datetime
from app import db


class ProjectInquiry(db.Model):
    __tablename__ = "project_inquiries"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profiles.id", ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    work_description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(255), nullable=True)
    expected_start_date = db.Column(db.Date, nullable=True)
    approximate_budget = db.Column(db.Numeric(12, 2), nullable=True)
    currency = db.Column(db.String(3), default="INR")
    status = db.Column(db.String(30), default="new", index=True)
    # new, contacted, discussing, accepted, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    customer = db.relationship("CustomerProfile", back_populates="inquiries")
    professional = db.relationship("ProfessionalProfile", back_populates="inquiries")
    status_history = db.relationship("InquiryStatusHistory", back_populates="inquiry", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "professional_id": self.professional_id,
            "work_description": self.work_description,
            "location": self.location,
            "expected_start_date": self.expected_start_date.isoformat() if self.expected_start_date else None,
            "approximate_budget": float(self.approximate_budget) if self.approximate_budget else None,
            "currency": self.currency,
            "status": self.status,
            "customer_name": self.customer.full_name if self.customer else None,
            "professional_name": self.professional.full_name if self.professional else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class InquiryStatusHistory(db.Model):
    __tablename__ = "inquiry_status_history"

    id = db.Column(db.Integer, primary_key=True)
    inquiry_id = db.Column(db.Integer, db.ForeignKey("project_inquiries.id", ondelete="CASCADE"), nullable=False)
    old_status = db.Column(db.String(30), nullable=True)
    new_status = db.Column(db.String(30), nullable=False)
    changed_by_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    note = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    inquiry = db.relationship("ProjectInquiry", back_populates="status_history")
