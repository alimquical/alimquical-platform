"""
Seed script - Crea el admin principal y datos iniciales.
Uso: python scripts/seed_admin.py
Configura las variables en .env antes de ejecutar.
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.database import SessionLocal, engine, Base
from core.security import get_password_hash
from models.user import User, UserRole
from models.company import Company
from models.subscription import Subscription
from datetime import datetime, timezone, timedelta


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    admin_email = os.getenv("ADMIN_EMAIL", "admin@alimquical.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "Admin123!")
    admin_name = os.getenv("ADMIN_NAME", "Super Admin")

    existing = db.query(User).filter(User.email == admin_email).first()
    if existing:
        print(f"[OK] Admin ya existe: {admin_email}")
        db.close()
        return

    company = Company(
        name="Alimquical Corp",
        plan="corporate",
        meetings_limit=99999,
        users_limit=9999,
    )
    db.add(company)
    db.flush()

    admin = User(
        email=admin_email,
        name=admin_name,
        hashed_password=get_password_hash(admin_password),
        role=UserRole.ADMIN,
        company_id=company.id,
        is_active=True,
    )
    db.add(admin)
    db.flush()

    sub = Subscription(
        company_id=company.id,
        plan="corporate",
        status="active",
        price=0,
        interval="monthly",
        current_period_start=datetime.now(timezone.utc),
        current_period_end=datetime.now(timezone.utc) + timedelta(days=365 * 10),
    )
    db.add(sub)
    db.commit()

    print(f"\n{'='*50}")
    print(f"  ADMIN CREADO EXITOSAMENTE")
    print(f"{'='*50}")
    print(f"  Email:    {admin_email}")
    print(f"  Password: {admin_password}")
    print(f"  Rol:      admin (superadmin)")
    print(f"  Empresa:  Alimquical Corp")
    print(f"  Plan:     Corporate (ilimitado)")
    print(f"{'='*50}")
    print(f"\n  GUARDA ESTAS CREDENCIALES EN LUGAR SEGURO")
    print(f"{'='*50}\n")

    db.close()


if __name__ == "__main__":
    seed()
