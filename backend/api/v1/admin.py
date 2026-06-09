import logging
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
from core.security import get_password_hash
logger = logging.getLogger(__name__)

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


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    company_name: str
    plan: str = "starter"
    role: str = "user"
    meetings_limit: int = 50
    users_limit: int = 5


class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


class PlanUpdate(BaseModel):
    plan: str
    meetings_limit: int = 50
    users_limit: int = 5


@router.post("/users", status_code=201)
def create_user(data: UserCreate, admin: User = Depends(get_current_admin), db: Session = Depends(get_db)):
    try:
        existing = db.query(User).filter(User.email == data.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="El correo ya está registrado")
        company = Company(name=data.company_name, plan=data.plan, meetings_limit=data.meetings_limit, users_limit=data.users_limit)
        db.add(company); db.flush()
        sub = Subscription(company_id=company.id, plan=data.plan, status="active")
        db.add(sub)
        user = User(email=data.email, name=data.name, hashed_password=get_password_hash(data.password), role=UserRole(data.role), company_id=company.id)
        db.add(user); db.commit(); db.refresh(user)
        return {"id": user.id, "email": user.email, "name": user.name, "role": user.role.value, "company_id": user.company_id}
    except Exception as e:
        logger.error("Error creando usuario", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


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
