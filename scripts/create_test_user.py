"""
Crea un usuario de prueba para verificar suscripciones.
python scripts/create_test_user.py
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from core.database import SessionLocal, Base, engine
from core.security import get_password_hash
from models.user import User, UserRole
from models.company import Company
from models.subscription import Subscription
from datetime import datetime, timezone, timedelta


def create_test_user(plan="starter"):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    limits = {
        "starter": {"meetings": 50, "users": 1, "price": 29.99},
        "business": {"meetings": 500, "users": 10, "price": 99.99},
        "corporate": {"meetings": 99999, "users": 9999, "price": 299.99},
    }

    cfg = limits[plan]

    company = Company(
        name=f"Empresa Demo ({plan})",
        plan=plan,
        meetings_limit=cfg["meetings"],
        users_limit=cfg["users"],
    )
    db.add(company)
    db.flush()

    user = User(
        email=f"usuario@{plan}.com",
        name=f"Usuario {plan.title()}",
        hashed_password=get_password_hash("Demo123!"),
        role=UserRole.USER,
        company_id=company.id,
        is_active=True,
    )
    db.add(user)
    db.flush()

    sub = Subscription(
        company_id=company.id,
        plan=plan,
        status="active",
        price=cfg["price"],
        interval="monthly",
        current_period_start=datetime.now(timezone.utc),
        current_period_end=datetime.now(timezone.utc) + timedelta(days=30),
    )
    db.add(sub)
    db.commit()

    print(f"\n[OK] Usuario {plan} creado:")
    print(f"  Email:    usuario@{plan}.com")
    print(f"  Password: Demo123!")
    print(f"  Plan:     {plan} (${cfg['price']}/mes)")
    print(f"  Límites:  {cfg['meetings']} reuniones, {cfg['users']} usuarios")

    db.close()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--plan", default="starter", choices=["starter", "business", "corporate"])
    args = parser.parse_args()
    create_test_user(args.plan)
