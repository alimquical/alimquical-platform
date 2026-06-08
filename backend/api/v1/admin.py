from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import decode_token
from models.user import User, UserRole
from models.company import Company
from models.subscription import Subscription
from pydantic import BaseModel
from typing import Optional
from fastapi import Header

router = APIRouter(prefix="/admin", tags=["admin"])


def get_current_admin(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    payload = decode_token(authorization.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user or user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Se requiere rol admin")
    return user


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class PlanUpdate(BaseModel):
    plan: str
    meetings_limit: int = 50
    users_limit: int = 5


@router.get("/users")
def list_users(admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).all()
    result = []
    for u in users:
        company = db.query(Company).filter(Company.id == u.company_id).first()
        sub = db.query(Subscription).filter(Subscription.company_id == u.company_id).first()
        result.append({
            "id": u.id,
            "email": u.email,
            "name": u.name,
            "role": u.role.value,
            "is_active": u.is_active,
            "company_name": company.name if company else None,
            "plan": sub.plan if sub else "none",
            "subscription_status": sub.status if sub else "inactive",
            "created_at": str(u.created_at),
        })
    return result


@router.put("/users/{user_id}")
def update_user(user_id: str, data: UserUpdate, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if data.name is not None:
        user.name = data.name
    if data.role is not None:
        user.role = UserRole(data.role)
    if data.is_active is not None:
        user.is_active = data.is_active
    db.commit()
    return {"msg": "Usuario actualizado"}


@router.delete("/users/{user_id}")
def delete_user(user_id: str, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail="No puedes eliminarte a ti mismo")
    db.delete(user)
    db.commit()
    return {"msg": "Usuario eliminado"}


@router.put("/users/{user_id}/plan")
def update_user_plan(user_id: str, plan: PlanUpdate, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    company.plan = plan.plan
    company.meetings_limit = plan.meetings_limit
    company.users_limit = plan.users_limit
    sub = db.query(Subscription).filter(Subscription.company_id == user.company_id).first()
    if sub:
        sub.plan = plan.plan
    db.commit()
    return {"msg": "Plan actualizado"}
