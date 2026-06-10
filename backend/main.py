from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from sqlalchemy.orm import Session
from core.config import settings
from core.database import engine, Base, SessionLocal
from core.security import get_password_hash
from models.user import User, UserRole
from models.company import Company
from api.v1.auth import router as auth_router
from api.v1.meetings import router as meetings_router
from api.v1.admin import router as admin_router
from api.v1.payments import router as payments_router
from api.v1.agents import router as agents_router
from api.v1.dashboard import router as dashboard_router

if settings.SENTRY_DSN:
    try:
        import sentry_sdk
        sentry_sdk.init(dsn=settings.SENTRY_DSN, environment=settings.ENVIRONMENT)
    except ImportError:
        pass


def seed_admin():
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@alimquical.com").first()
        if not existing:
            company = Company(name="Alimquical Inc", plan="enterprise", meetings_limit=9999, users_limit=100)
            db.add(company); db.flush()
            user = User(email="admin@alimquical.com", name="Admin", hashed_password=get_password_hash("Admin123!"), role=UserRole.ADMIN, company_id=company.id)
            db.add(user); db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_admin()
    from agents import init_agents
    init_agents()
    yield


app = FastAPI(lifespan=lifespan,
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.WHITELIST_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*", "appmovilvercel.vercel.app", "frontend-dusky-chi-71.vercel.app"],
)

app.include_router(auth_router, prefix="/api/v1")
app.include_router(meetings_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")
app.include_router(payments_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(dashboard_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": settings.VERSION, "environment": settings.ENVIRONMENT}


@app.get("/")
def root():
    return {"message": "Alimquical AI Executive Platform API", "version": settings.VERSION}
