from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MeetingCreate(BaseModel):
    title: str
    date: datetime
    duration: int = 60
    participants: Optional[str] = None


class MeetingResponse(BaseModel):
    id: str
    title: str
    date: datetime
    duration: int
    status: str
    transcript: Optional[str] = None
    summary: Optional[str] = None
    participants: Optional[str] = None
    company_id: str
    created_at: datetime

    model_config = {"from_attributes": True}
