from enum import Enum

from typing import Optional

from click import Option
from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import date, datetime


class TriageModes(str, Enum):
    Document_Only = ("document",)
    Symptom_Only = ("general",)
    Both = "triage"


class Result(str, Enum):
    green = ("green",)
    yellow = ("yellow",)
    red = "red"


class Language(str, Enum):
    arabic = "AR"
    english = "EN"


class Status(str, Enum):
    in_progress = ("in_progress",)
    completed = ("completed",)
    abandoned = "abandoned"


class ChatCreationValidation(BaseModel):
    mode: TriageModes
    report_id: Optional[str] = None


class GuestChatCreationValidation(BaseModel):
    mode: TriageModes


class ChatListValidation(BaseModel):
    mode: Optional[str] = None
    offset: int
    limit: int


class ChatMessageValidation(BaseModel):
    message: str


class ChatResponse(BaseModel):
    id: str
    mode: TriageModes
    title: str
    report_id: Optional[str]
    report_type: Optional[str]
    triage_result: Optional[str]
    message_count: str
    last_message_at: str
    language: str


class ChatSessionObject(BaseModel):
    id: Optional[UUID]
    user_id: Optional[UUID]
    report_id: Optional[UUID]
    mode: TriageModes
    title: Optional[str]
    language: Optional[Language] = "EN"
    is_guest: Optional[bool] = False
    guest_token: Optional[UUID] = None
    triage_status: Status
    triage_result: Optional[Result]
    triage_completed_at: Optional[datetime] = None
    created_at: Optional[str] = None
    last_message_at: Optional[str] = None
