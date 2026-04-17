import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from app.db.base import Base

class PatientDemographics(Base):
    __tablename__ = "patient_demographics"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id: UUID FK - References USERS.id. DELETE CASCADE
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        unique=True, # One demographic profile per user
        nullable=False,
        index=True
    )

    # age_range: 18-25 | 26-35 | 36-45 | 46-55 | 56-65 | 65+
    age_range = Column(
        Enum(
            "18-25", "26-35", "36-45", "46-55", "56-65", "65+", 
            name="age_range_enum"
        ),
        nullable=False
    )

    # gender: male | female | prefer_not_to_say
    gender = Column(
        Enum("male", "female", "prefer_not_to_say", name="gender_enum"),
        nullable=False
    )

    # nationality: ISO 3166-1 alpha-2 (e.g., 'SA', 'AE', 'IN')
    nationality = Column(String(2), nullable=False)

    # region: riyadh | jeddah | eastern_province | dubai | abu_dhabi | other
    region = Column(
        Enum(
            "riyadh", "jeddah", "eastern_province", 
            "dubai", "abu_dhabi", "other", 
            name="region_enum"
        ),
        nullable=False
    )

    # health_literacy: low | medium | high
    health_literacy = Column(
        Enum("low", "medium", "high", name="health_literacy_enum"),
        nullable=False
    )

    # chronic_conditions: JSONB [diabetes, hypertension]
    chronic_conditions = Column(JSONB, nullable=True, default=[])

    # Research Consent (PDPL Requirements)
    consent_for_research = Column(Boolean, default=False, nullable=False)
    consent_given_at = Column(DateTime(timezone=True), nullable=True)

    # Audit Timestamp
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    def __repr__(self):
        return f"<PatientDemographics(user_id={self.user_id}, region={self.region})>"