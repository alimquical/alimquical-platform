from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timezone, date
from core.database import get_db
from core.security import decode_token
from models.user import User
from models.meeting import Meeting, MeetingStatus
from models.task import Task, TaskStatus
from models.client import Client, ClientStatus
from models.document import Document
from models.company import Company

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


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


@router.get("/overview")
def dashboard_overview(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = user.company_id
    now = datetime.now(timezone.utc)

    total_meetings = db.query(func.count(Meeting.id)).filter(Meeting.company_id == company_id).scalar() or 0
    pending_meetings = db.query(func.count(Meeting.id)).filter(
        Meeting.company_id == company_id, Meeting.status == MeetingStatus.SCHEDULED,
        Meeting.date >= now
    ).scalar() or 0
    recent_meetings = db.query(func.count(Meeting.id)).filter(
        Meeting.company_id == company_id, Meeting.status == MeetingStatus.COMPLETED,
        Meeting.date >= now.replace(hour=0, minute=0, second=0)  # today
    ).scalar() or 0

    total_tasks = db.query(func.count(Task.id)).filter(Task.company_id == company_id).scalar() or 0
    active_tasks = db.query(func.count(Task.id)).filter(
        Task.company_id == company_id, Task.status != TaskStatus.DONE
    ).scalar() or 0
    overdue_tasks = db.query(func.count(Task.id)).filter(
        Task.company_id == company_id, Task.status != TaskStatus.DONE,
        Task.due_date < date.today()
    ).scalar() or 0

    active_clients = db.query(func.count(Client.id)).filter(
        Client.company_id == company_id, Client.status == ClientStatus.ACTIVE
    ).scalar() or 0
    total_clients = db.query(func.count(Client.id)).filter(Client.company_id == company_id).scalar() or 0

    total_documents = db.query(func.count(Document.id)).filter(Document.company_id == company_id).scalar() or 0

    company = db.query(Company).filter(Company.id == company_id).first()

    return {
        "meetings": {
            "total": total_meetings,
            "pending": pending_meetings,
            "recent_today": recent_meetings,
        },
        "tasks": {
            "total": total_tasks,
            "active": active_tasks,
            "overdue": overdue_tasks,
        },
        "clients": {
            "total": total_clients,
            "active": active_clients,
        },
        "documents": {
            "total": total_documents,
        },
        "company": {
            "name": company.name if company else "",
            "plan": company.plan if company else "",
        },
    }


@router.get("/activity")
def dashboard_activity(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = user.company_id

    recent_meetings = (
        db.query(Meeting)
        .filter(Meeting.company_id == company_id)
        .order_by(Meeting.date.desc())
        .limit(5)
        .all()
    )

    return [
        {
            "id": m.id,
            "type": "meeting",
            "title": m.title,
            "date": m.date.isoformat(),
            "status": m.status.value,
            "participants": m.participants,
        }
        for m in recent_meetings
    ]


@router.get("/tasks")
def dashboard_tasks(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = user.company_id

    tasks = (
        db.query(Task)
        .filter(Task.company_id == company_id)
        .order_by(Task.created_at.desc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": t.id,
            "title": t.title,
            "status": t.status.value,
            "priority": t.priority.value,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "created_at": t.created_at.isoformat(),
        }
        for t in tasks
    ]


@router.get("/calendar")
def dashboard_calendar(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = user.company_id

    upcoming = (
        db.query(Meeting)
        .filter(
            Meeting.company_id == company_id,
            Meeting.status == MeetingStatus.SCHEDULED,
            Meeting.date >= datetime.now(timezone.utc),
        )
        .order_by(Meeting.date.asc())
        .limit(10)
        .all()
    )

    return [
        {
            "id": m.id,
            "title": m.title,
            "date": m.date.isoformat(),
            "duration": m.duration,
            "participants": m.participants,
        }
        for m in upcoming
    ]


@router.get("/notifications")
def dashboard_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    company_id = user.company_id
    alerts = []

    overdue_tasks = (
        db.query(Task)
        .filter(
            Task.company_id == company_id,
            Task.status != TaskStatus.DONE,
            Task.due_date < date.today(),
        )
        .count()
    )
    if overdue_tasks:
        alerts.append({
            "type": "warning",
            "message": f"Tienes {overdue_tasks} tareas vencidas",
        })

    pending_meetings = (
        db.query(Meeting)
        .filter(
            Meeting.company_id == company_id,
            Meeting.status == MeetingStatus.SCHEDULED,
            Meeting.date >= datetime.now(timezone.utc),
        )
        .count()
    )
    if pending_meetings:
        alerts.append({
            "type": "info",
            "message": f"Tienes {pending_meetings} reuniones programadas",
        })

    return alerts
