import uuid
from sqlalchemy import Column, String, Numeric, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from db.base import Base

class LabValue(Base):
    __tablename__ = "lab_values"

    # id: UUID PK
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # report_id: UUID FK - References REPORTS.id
    report_id = Column(
        UUID(as_uuid=True), 
        ForeignKey("reports.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )

    # panel_name: Grouping for UI (CBC, Lipid Panel, etc.)
    panel_name = Column(String(100), nullable=False)

    # test_category: Broader grouping (haematology, biochemistry, etc.)
    # Note: 'cardiac_enzymes' triggers special flags in your logic
    test_category = Column(String(50), nullable=False, index=True)

    # test_name: Original name (e.g., "Hemoglobin")
    test_name = Column(String(255), nullable=False)

    # value: Exact numeric value (Never rounded)
    value = Column(Numeric, nullable=True)

    # unit: e.g., g/dL, mmol/L
    unit = Column(String(50), nullable=True)

    # Reference Ranges
    normal_range_low = Column(Numeric, nullable=True)
    normal_range_high = Column(Numeric, nullable=True)

    # flag: ENUM for status categorization
    flag = Column(
        Enum(
            "normal", "low", "high", 
            "borderline_low", "borderline_high", "critical", 
            name="lab_flag_enum"
        ),
        nullable=False,
        default="normal"
    )

    # extracted_language: Language of test_name in report
    extracted_language = Column(String(10), nullable=False, default="en")

    def __repr__(self):
        return f"<LabValue(test={self.test_name}, value={self.value}, flag={self.flag})>"