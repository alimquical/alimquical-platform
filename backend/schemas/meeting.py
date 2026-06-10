from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MeetingCreate(BaseModel):
    title: str
    date: datetime
    duration: int = 60
    participants: Optional[str] = None


class MeetingUpdate(BaseModel):
    title: Optional[str] = None
    date: Optional[datetime] = None
    duration: Optional[int] = None
    status: Optional[str] = None
    participants: Optional[str] = None
    summary: Optional[str] = None
    transcript: Optional[str] = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    date: datetime
    duration: int
    status: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    participants: Optional[str] = None
    recording_url: Optional[str] = None
    recording_duration: Optional[int] = None
    company_id: str
    created_by: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
