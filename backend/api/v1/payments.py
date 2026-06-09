from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from core.database import get_db
from core.config import settings
from models.user import User, UserRole
from models.company import Company
from models.subscription import Subscription
from services import get_available_gateways, get_default_gateway, get_gateway
from api.v1.admin import get_current_admin
from datetime import datetime, timezone, timedelta

router = APIRouter(prefix="/payments", tags=["payments"])


class CreateLinkRequest(BaseModel):
    user_id: str
    gateway: Optional[str] = None
    return_url: str = "https://frontend-dusky-chi-71.vercel.app/dashboard"


@router.post("/create-link")
def create_payment_link(
    data: CreateLinkRequest,
    admin: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    company = db.query(Company).filter(Company.id == user.company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Empresa no encontrada")
    sub = db.query(Subscription).filter(Subscription.company_id == user.company_id).first()
    plan = sub.plan if sub else "starter"

    gateway = get_gateway(data.gateway) if data.gateway else get_default_gateway()
    if not gateway:
        raise HTTPException(status_code=503, detail="No hay pasarela de pago disponible")

    result = gateway.create_payment_link(
        company_name=company.name,
        plan=plan,
        email=user.email,
        user_id=user.id,
        company_id=user.company_id,
        return_url=data.return_url,
    )
    if not result.success:
        raise HTTPException(status_code=502, detail=result.error or "Error al generar link")

    return {
        "payment_url": result.payment_url,
        "payment_id": result.payment_id,
        "gateway": result.gateway,
    }


@router.post("/webhook")
async def payments_webhook(request: Request, db: Session = Depends(get_db)):
    raw_body = await request.body()
    body = await request.json()
    headers = dict(request.headers)

    for gateway in get_available_gateways():
        result = gateway.process_webhook(body, raw_body, headers)
        if result.success and result.company_id:
            sub = db.query(Subscription).filter(Subscription.company_id == result.company_id).first()
            if sub:
                now = datetime.now(timezone.utc)
                sub.status = "active"
                sub.current_period_start = now
                sub.current_period_end = now + timedelta(days=30)
                sub.payment_gateway = result.gateway
                if result.gateway == "stripe":
                    sub.stripe_subscription_id = result.payment_id
                if result.gateway == "mercadopago":
                    sub.mercadopago_payment_id = result.payment_id
            company = db.query(Company).filter(Company.id == result.company_id).first()
            if company:
                company.plan = result.plan or company.plan
            db.commit()
            break
    return {"status": "ok"}


@router.get("/gateways")
def list_gateways():
    return [
        {"name": g.name, "available": g.is_available()}
        for g in get_available_gateways()
    ]