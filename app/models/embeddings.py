import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from pgvector.sqlalchemy import Vector # Requires pgvector python package
from db.base import Base

class ReportEmbedding(Base):
    __tablename__ = "embeddings"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # report_id: UUID FK
    # Scopes search to one patient's report (Never global)
    report_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("reports.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # chunk_text: AES-256 encrypted PHI
    chunk_text_enc = Column(Text, nullable=False)

    # embedding_vector: Float[768] from text-multilingual-embedding-002
    # CMEK protected at DB level
    embedding_vector = Column(Vector(768), nullable=False)

    # chunk_index: Position in document for context reconstruction
    chunk_index = Column(Integer, nullable=False)

    # section_name: Panel name (CBC, Lipid Panel, etc.)
    # Used for round-robin panel coverage retrieval
    section_name = Column(String(100), nullable=True)

    # token_count: Target 400, max 440
    token_count = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<ReportEmbedding(report_id={self.report_id}, index={self.chunk_index}, tokens={self.token_count})>"