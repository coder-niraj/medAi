import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Text, SmallInteger, Integer
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base

class ClinicianReview(Base):
    __tablename__ = "clinician_reviews"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # message_id: UUID FK - References CHAT_MESSAGES.id
    message_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("chat_messages.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # reviewer_id: UUID FK - References USERS.id (Must be a doctor)
    reviewer_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id"), 
        nullable=False,
        index=True
    )

    # Ratings (1-5 scale)
    accuracy_rating = Column(SmallInteger, nullable=False) # 1=dangerous, 5=excellent
    safety_rating = Column(SmallInteger, nullable=False)   # 1=unsafe, 5=fully safe
    completeness_rating = Column(SmallInteger, nullable=False) # 1=missing info, 5=complete

    # Error Tracking
    contains_error = Column(Boolean, default=False, nullable=False)
    error_description = Column(Text, nullable=True)
    suggested_correction = Column(Text, nullable=True)

    # Training Logic
    # Final signal written back to FINE_TUNING_EXAMPLES.clinician_validated
    is_safe_to_train_on = Column(Boolean, default=False, nullable=False)

    # Audit & Quality Metadata
    reviewed_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    # flag rushed reviews under 30 seconds
    review_duration_sec = Column(Integer, nullable=True)

    def __repr__(self):
        return f"<ClinicianReview(msg_id={self.message_id}, safe={self.is_safe_to_train_on})>"