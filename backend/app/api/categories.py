from flask import Blueprint, jsonify
from app.models import ServiceCategory

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("", methods=["GET"])
def list_categories():
    cats = (
        ServiceCategory.query.filter_by(is_active=True)
        .order_by(ServiceCategory.sort_order, ServiceCategory.name)
        .all()
    )
    return jsonify([c.to_dict() for c in cats])


@categories_bp.route("/<slug>", methods=["GET"])
def get_category(slug):
    cat = ServiceCategory.query.filter_by(slug=slug, is_active=True).first_or_404()
    return jsonify(cat.to_dict())
