import os
import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File, Form, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from core.database import get_db
from core.security import decode_token
from models.user import User
from models.meeting import Meeting, MeetingStatus
from schemas.meeting import MeetingCreate, MeetingUpdate, MeetingResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/meetings", tags=["meetings"])

RECORDINGS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)


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


@router.get("/", response_model=List[MeetingResponse])
def list_meetings(
    skip: int = 0,
    limit: int = 50,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meetings = (
        db.query(Meeting)
        .filter(Meeting.company_id == user.company_id)
        .order_by(Meeting.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return meetings


@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(
    meeting: MeetingCreate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db_meeting = Meeting(
        title=meeting.title,
        date=meeting.date,
        duration=meeting.duration,
        participants=meeting.participants,
        company_id=user.company_id,
        created_by=user.id,
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(
    meeting_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.company_id == user.company_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    return meeting


@router.put("/{meeting_id}", response_model=MeetingResponse)
def update_meeting(
    meeting_id: str,
    data: MeetingUpdate,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.company_id == user.company_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    for field, value in data.model_dump(exclude_none=True).items():
        if field == "status":
            value = MeetingStatus(value)
        setattr(meeting, field, value)
    db.commit()
    db.refresh(meeting)
    return meeting


@router.delete("/{meeting_id}")
def delete_meeting(
    meeting_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.company_id == user.company_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    if meeting.recording_url:
        rec_path = os.path.join(RECORDINGS_DIR, os.path.basename(meeting.recording_url))
        if os.path.exists(rec_path):
            os.remove(rec_path)
    db.delete(meeting)
    db.commit()
    return {"msg": "Reunión eliminada"}


@router.post("/{meeting_id}/recording")
def upload_recording(
    meeting_id: str,
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.company_id == user.company_id).first()
    if not meeting:
        raise HTTPException(status_code=404, detail="Reunión no encontrada")
    ext = os.path.splitext(file.filename or "audio.webm")[1] or ".webm"
    filename = f"{meeting_id}_{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(RECORDINGS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    meeting.recording_url = f"/api/v1/meetings/{meeting_id}/recording"
    db.commit()
    return {"recording_url": meeting.recording_url}


@router.get("/{meeting_id}/recording")
def get_recording(
    meeting_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id, Meeting.company_id == user.company_id).first()
    if not meeting or not meeting.recording_url:
        raise HTTPException(status_code=404, detail="Grabación no encontrada")
    filename = os.path.basename(meeting.recording_url)
    filepath = os.path.join(RECORDINGS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Archivo no encontrado")
    return FileResponse(filepath, media_type="audio/webm", filename=filename)
