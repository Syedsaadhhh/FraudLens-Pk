import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class ScanRecordDB(SQLModel, table=True):
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        index=True
    )
    createdAt: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    inputType: str
    maskedInput: str
    riskLevel: str
    confidence: int
    scamType: str
    summary: str
    redFlags: str          # Stored as JSON string
    suspiciousPhrases: str  # Stored as JSON string
    englishExplanation: str
    urduExplanation: str
    safeActions: str        # Stored as JSON string
    doNotDo: str             # Stored as JSON string
    reportText: Optional[str] = Field(default=None, nullable=True)
