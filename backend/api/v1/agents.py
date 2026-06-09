from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import decode_token
from fastapi import Header
from models.user import User, UserRole
from agents import get_agent, get_all_agents, list_agents, init_agents
from agents.base import AgentRequest, AgentContext
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/agents", tags=["agents"])


def get_current_user(authorization: str = Header(...), db: Session = Depends(get_db)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token requerido")
    payload = decode_token(authorization.split(" ")[1])
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    user = db.query(User).filter(User.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


class AgentChatRequest(BaseModel):
    agent: str = "chief"
    query: str
    action: Optional[str] = None
    params: dict = {}


@router.get("/list")
def list_agents_endpoint():
    return list_agents()


@router.post("/chat")
async def chat_with_agent(req: AgentChatRequest, user: User = Depends(get_current_user)):
    agent = get_agent(req.agent)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agente '{req.agent}' no encontrado")

    context = AgentContext(
        company_id=user.company_id or "",
        user_id=user.id,
        user_role=user.role.value if hasattr(user.role, "value") else str(user.role),
    )

    agent_req = AgentRequest(
        action=req.action or req.query,
        params={"query": req.query, **req.params},
        context=context,
    )

    result = await agent.process(agent_req)
    if not result.success:
        raise HTTPException(status_code=502, detail=result.error or "Error del agente")

    return {"message": result.message, "data": result.data, "agent": agent.role.value}


@router.post("/chief")
async def chief_agent(req: AgentChatRequest, user: User = Depends(get_current_user)):
    req.agent = "chief"
    return await chat_with_agent(req, user)
