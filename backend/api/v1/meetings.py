from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from core.database import get_db
from models.meeting import Meeting, MeetingStatus
from schemas.meeting import MeetingCreate, MeetingResponse

router = APIRouter(prefix="/meetings", tags=["meetings"])


@router.get("/", response_model=List[MeetingResponse])
def list_meetings(
    company_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    meetings = (
        db.query(Meeting)
        .filter(Meeting.company_id == company_id)
        .order_by(Meeting.date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )
    return meetings


@router.post("/", response_model=MeetingResponse, status_code=status.HTTP_201_CREATED)
def create_meeting(meeting: MeetingCreate, company_id: str, user_id: str, db: Session = Depends(get_db)):
    db_meeting = Meeting(
        title=meeting.title,
        date=meeting.date,
        duration=meeting.duration,
        participants=meeting.participants,
        company_id=company_id,
        created_by=user_id,
    )
    db.add(db_meeting)
    db.commit()
    db.refresh(db_meeting)
    return db_meeting


@router.get("/{meeting_id}", response_model=MeetingResponse)
def get_meeting(meeting_id: str, db: Session = Depends(get_db)):
    meeting = db.query(Meeting).filter(Meeting.id == meeting_id).first()
    if not meeting:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Reunión no encontrada")
    return meeting
