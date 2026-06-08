import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from core.database import Base, engine, SessionLocal
from core.security import get_password_hash
from models.user import User, UserRole
from models.company import Company
from models.subscription import Subscription
from datetime import datetime, timezone, timedelta

Base.metadata.create_all(bind=engine)
db = SessionLocal()

admin_email = os.getenv("ADMIN_EMAIL", "admin@alimquical.com")
admin_password = os.getenv("ADMIN_PASSWORD", "Admin123!")

existing = db.query(User).filter(User.email == admin_email).first()
if existing:
    print(f"Admin ya existe: {admin_email}")
else:
    company = Company(name="Alimquical Corp", plan="corporate", meetings_limit=99999, users_limit=9999)
    db.add(company); db.flush()
    admin = User(email=admin_email, name="Super Admin", hashed_password=get_password_hash(admin_password), role=UserRole.ADMIN, company_id=company.id, is_active=True)
    db.add(admin); db.flush()
    sub = Subscription(company_id=company.id, plan="corporate", status="active", price=0, interval="monthly", current_period_start=datetime.now(timezone.utc), current_period_end=datetime.now(timezone.utc) + timedelta(days=365*10))
    db.add(sub); db.commit()
    print(f"Admin creado: {admin_email} / {admin_password}")

for u in db.query(User).all():
    print(f"  Usuario: {u.email} | Rol: {u.role.value} | Activo: {u.is_active}")
db.close()
