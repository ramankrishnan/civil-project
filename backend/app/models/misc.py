from datetime import datetime
from app import db


class SavedProfessional(db.Model):
    __tablename__ = "saved_professionals"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profiles.id", ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("CustomerProfile", back_populates="saved_professionals")
    professional = db.relationship("ProfessionalProfile")

    __table_args__ = (db.UniqueConstraint("customer_id", "professional_id", name="uq_saved_prof"),)


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer_profiles.id", ondelete="CASCADE"), nullable=False)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    inquiry_id = db.Column(db.Integer, db.ForeignKey("project_inquiries.id"), nullable=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text, nullable=True)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship("CustomerProfile", back_populates="reviews")
    professional = db.relationship("ProfessionalProfile", back_populates="reviews")

    def to_dict(self):
        return {
            "id": self.id,
            "customer_name": self.customer.full_name if self.customer else "Anonymous",
            "rating": self.rating,
            "comment": self.comment,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(db.Integer, primary_key=True)
    reporter_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    reported_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    reported_profile_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id"), nullable=True)
    reason = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default="pending")  # pending, reviewed, resolved, dismissed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    reporter = db.relationship("User", foreign_keys=[reporter_id], back_populates="reports_made")


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=True)  # inquiry, verification, system
    is_read = db.Column(db.Boolean, default=False)
    link = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="notifications")

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "message": self.message,
            "type": self.type,
            "is_read": self.is_read,
            "link": self.link,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class VerificationRequest(db.Model):
    __tablename__ = "verification_requests"

    id = db.Column(db.Integer, primary_key=True)
    professional_id = db.Column(db.Integer, db.ForeignKey("professional_profiles.id", ondelete="CASCADE"), nullable=False)
    document_type = db.Column(db.String(50), nullable=False)  # id_proof, license, certificate
    document_url = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(30), default="pending")  # pending, approved, rejected
    admin_note = db.Column(db.Text, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    professional = db.relationship("ProfessionalProfile", back_populates="verification_requests")


class AdminAuditLog(db.Model):
    __tablename__ = "admin_audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    target_type = db.Column(db.String(50), nullable=True)
    target_id = db.Column(db.Integer, nullable=True)
    details = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
