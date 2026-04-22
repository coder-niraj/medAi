import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum, Date
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    name = Column(String(255), nullable=False)

    email_enc = Column(String, nullable=False)
    phone_enc = Column(String, nullable=True)
    dob_enc = Column(String, nullable=True)
    preferred_language = Column(String(10), nullable=False, default="en")
    role = Column(
        Enum("patient", "doctor", "admin", name="role_enum"),
        nullable=False,
        default="patient",
    )

    firebase_uid = Column(String(255), unique=True, index=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True), default=datetime.utcnow, nullable=False
    )

    consent_given_at = Column(DateTime(timezone=True), nullable=True)

    research_consent = Column(Boolean, default=False, nullable=False)

    triage_count = Column(Integer, default=0, nullable=False)
