# NirmanConnect

**Find the Right Professional for Your Next Project**

NirmanConnect is a complete construction & local services marketplace that connects property owners, homeowners, and builders with civil engineers, masons, electricians, plumbers, painters, carpenters, and other skilled professionals across India.

Customers discover and contact professionals directly. The platform does **not** automatically assign jobs. Pricing and terms are agreed between the customer and the professional.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | React 18 + TypeScript + Vite + Tailwind CSS + React Router |
| Backend | Python Flask + SQLAlchemy + Flask-Migrate + Flask-JWT-Extended |
| Database | PostgreSQL |
| Auth | JWT (access + refresh tokens) + role-based access control |
| File Storage | Azure Blob Storage (local fallback for development) |
| Deployment | Docker + Docker Compose + Azure App Service / Container Apps |
| CI/CD | GitHub Actions |

## Project Structure

```
NirmanConnect/
├── backend/                 # Flask API
│   ├── app/
│   │   ├── api/             # Route blueprints
│   │   ├── models/          # SQLAlchemy models
│   │   ├── services/        # Business logic
│   │   └── utils/           # Helpers, validators
│   ├── migrations/          # Alembic migrations
│   ├── tests/               # Pytest tests
│   ├── scripts/             # Seed data, utilities
│   ├── Dockerfile
│   ├── requirements.txt
│   └── run.py
├── frontend/                # React + Vite app
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/        # API clients
│   │   ├── context/         # Auth context
│   │   └── types/
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.ts
├── docs/                    # Architecture & API docs
├── .github/workflows/       # CI pipeline
├── docker-compose.yml
├── .env.example
└── README.md
```

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.11+
- PostgreSQL 15+ (or use Docker)

### 1. Clone & Configure

```bash
git clone <your-repo-url>
cd NirmanConnect
cp .env.example .env
# Edit .env with your values (see comments)
```

### 2. Start with Docker Compose (recommended)

```bash
docker-compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:5000
- PostgreSQL: localhost:5432

### 3. Manual Setup (without Docker)

**Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export FLASK_APP=run.py
flask db upgrade
python scripts/seed_data.py
flask run --host=0.0.0.0 --port=5000
```

**Frontend**
```bash
cd frontend
npm install
npm run dev
```

### 4. Default Accounts (seed data – fictional)

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@nirmanconnect.com | Admin@12345 |
| Customer | customer@example.com | Customer@123 |
| Professional | mason@example.com | Worker@123 |

## Key Features Implemented

- Secure registration & login (Customer / Professional / Admin)
- Role-based dashboards
- Professional profiles with skills, experience, pricing, portfolio
- Real search & filtering (skill, city, PIN, experience, availability)
- Click-to-call & WhatsApp contact (consent-based)
- Project inquiry system with status tracking
- Saved professionals
- Admin moderation & verification workflow
- Responsive modern UI (mobile-first)
- Docker + Azure deployment ready

## Azure Deployment

See `docs/AZURE_DEPLOYMENT.md` for full instructions using:
- Azure Container Apps or App Service
- Azure Database for PostgreSQL
- Azure Blob Storage
- Azure Key Vault for secrets
- GitHub Actions for CI/CD

## API Documentation

See `docs/API.md` for endpoint reference with example requests/responses.

## Testing

```bash
# Backend
cd backend
pytest -v

# Frontend
cd frontend
npm test
```

## Known Limitations & Future Improvements

- Email/SMS/WhatsApp notifications are designed but require provider configuration
- Real-time chat is not included (future)
- Payment gateway integration is out of scope for v1
- Advanced analytics dashboard is basic
- Image optimization & CDN can be added later
- Multi-language support (Hindi + English) planned

## License

MIT – feel free to use and extend for learning or production.

---

Built with ❤️ for the Indian construction ecosystem.
