import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from db.base import Base

class ExtensionHook(Base):
    __tablename__ = "extension_hooks"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # user_id: UUID FK - References USERS.id. DELETE CASCADE
    # Useful if hooks are tenant-specific or user-specific settings
    user_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # hook_name: Unique name for the feature or integration
    # e.g., 'telemedicine_enabled', 'whatsapp_followup_enabled'
    hook_name = Column(String(100), nullable=False)

    # hook_value: Configuration payload (JSONB)
    # Allows for flexible schemas per hook_name
    hook_value = Column(JSONB, nullable=False, default={})

    # is_active: Feature flag toggle
    is_active = Column(Boolean, default=False, nullable=False)

    # Audit Timestamps
    created_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        nullable=False
    )
    
    updated_at = Column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc), 
        onupdate=lambda: datetime.now(timezone.utc), 
        nullable=False
    )

    # Constraint: Ensure a user doesn't have duplicate hooks of the same name
    __table_args__ = (
        UniqueConstraint('user_id', 'hook_name', name='_user_hook_uc'),
    )

    def __repr__(self):
        return f"<ExtensionHook(name={self.hook_name}, active={self.is_active})>"