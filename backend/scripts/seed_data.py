"""
Seed fictional development data for NirmanConnect.
Run: python scripts/seed_data.py
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import (
    User,
    CustomerProfile,
    ProfessionalProfile,
    ProfessionalSkill,
    ServiceCategory,
    PortfolioItem,
)

app = create_app()

CATEGORIES = [
    ("Civil Engineers", "civil-engineers", "🏗️", "Structural design, site supervision, project planning"),
    ("Masons", "masons", "🧱", "Brickwork, plastering, concrete work"),
    ("Electricians", "electricians", "⚡", "Wiring, fixtures, electrical repairs"),
    ("Plumbers", "plumbers", "🔧", "Pipes, fittings, bathroom & kitchen plumbing"),
    ("Painters", "painters", "🎨", "Interior & exterior painting, waterproofing"),
    ("Carpenters", "carpenters", "🪚", "Furniture, doors, windows, modular work"),
    ("Contractors", "contractors", "🏢", "Full construction & renovation contractors"),
    ("Tile Workers", "tile-workers", "🟦", "Flooring, wall tiles, marble & granite"),
    ("Interior Designers", "interior-designers", "🛋️", "Space planning, design consultation"),
    ("Welders", "welders", "🔥", "Metal fabrication, gates, grills"),
    ("Architects", "architects", "📐", "Building design, plans, approvals"),
    ("Cleaning & Maintenance", "cleaning-maintenance", "🧹", "Deep cleaning, facility maintenance"),
]


def seed():
    with app.app_context():
        # Categories
        if ServiceCategory.query.count() == 0:
            for i, (name, slug, icon, desc) in enumerate(CATEGORIES):
                db.session.add(
                    ServiceCategory(name=name, slug=slug, icon=icon, description=desc, sort_order=i)
                )
            db.session.commit()
            print("✅ Categories seeded")

        # Admin
        if not User.query.filter_by(email="admin@nirmanconnect.com").first():
            admin = User(email="admin@nirmanconnect.com", role="admin", phone="9999999999")
            admin.set_password("Admin@12345")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created")

        # Customer
        if not User.query.filter_by(email="customer@example.com").first():
            u = User(email="customer@example.com", role="customer", phone="9876543210")
            u.set_password("Customer@123")
            db.session.add(u)
            db.session.flush()
            db.session.add(
                CustomerProfile(
                    user_id=u.id,
                    full_name="Rahul Sharma",
                    city="Hyderabad",
                    locality="Gachibowli",
                    pin_code="500032",
                )
            )
            db.session.commit()
            print("✅ Sample customer created")

        # Professionals
        samples = [
            {
                "email": "mason@example.com",
                "phone": "9123456780",
                "name": "Ramesh Kumar",
                "city": "Hyderabad",
                "locality": "Madhapur",
                "pin": "500081",
                "exp": 12,
                "intro": "Experienced mason specializing in residential brickwork and plastering.",
                "pricing": "daily",
                "price": 800,
                "cat_slug": "masons",
                "verified": True,
            },
            {
                "email": "electrician@example.com",
                "phone": "9123456781",
                "name": "Suresh Reddy",
                "city": "Hyderabad",
                "locality": "Kukatpally",
                "pin": "500072",
                "exp": 8,
                "intro": "Licensed electrician for homes and small commercial spaces.",
                "pricing": "hourly",
                "price": 350,
                "cat_slug": "electricians",
                "verified": True,
            },
            {
                "email": "plumber@example.com",
                "phone": "9123456782",
                "name": "Vijay Singh",
                "city": "Secunderabad",
                "locality": "Trimulgherry",
                "pin": "500015",
                "exp": 10,
                "intro": "Reliable plumber for bathroom fittings, leaks and new installations.",
                "pricing": "per_project",
                "price": 2500,
                "cat_slug": "plumbers",
                "verified": False,
            },
            {
                "email": "painter@example.com",
                "phone": "9123456783",
                "name": "Anil Naidu",
                "city": "Hyderabad",
                "locality": "Banjara Hills",
                "pin": "500034",
                "exp": 15,
                "intro": "Interior & exterior painting with waterproofing expertise.",
                "pricing": "per_sqft",
                "price": 18,
                "cat_slug": "painters",
                "verified": True,
            },
            {
                "email": "civil@example.com",
                "phone": "9123456784",
                "name": "Priya Patel",
                "city": "Hyderabad",
                "locality": "Hitech City",
                "pin": "500081",
                "exp": 7,
                "intro": "Civil engineer offering structural consultation and site supervision.",
                "pricing": "negotiable",
                "price": None,
                "cat_slug": "civil-engineers",
                "verified": True,
            },
        ]

        for s in samples:
            if User.query.filter_by(email=s["email"]).first():
                continue
            u = User(email=s["email"], role="professional", phone=s["phone"])
            u.set_password("Worker@123")
            db.session.add(u)
            db.session.flush()
            prof = ProfessionalProfile(
                user_id=u.id,
                full_name=s["name"],
                city=s["city"],
                locality=s["locality"],
                pin_code=s["pin"],
                years_of_experience=s["exp"],
                introduction=s["intro"],
                pricing_type=s["pricing"],
                price_amount=s["price"],
                is_verified=s["verified"],
                verification_status="approved" if s["verified"] else "pending",
                show_phone_publicly=True,
                whatsapp_consent=True,
                availability="available",
            )
            db.session.add(prof)
            db.session.flush()
            cat = ServiceCategory.query.filter_by(slug=s["cat_slug"]).first()
            if cat:
                db.session.add(
                    ProfessionalSkill(professional_id=prof.id, category_id=cat.id, is_primary=True)
                )
        db.session.commit()
        print("✅ Sample professionals created")
        print("\n🎉 Seed complete! Use the accounts listed in README.")


if __name__ == "__main__":
    seed()
