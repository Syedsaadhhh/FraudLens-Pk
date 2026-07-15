import json
import logging
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlmodel import Session

from app.db import crud
from app.db.database import get_session
from app.models.db_models import ScanRecordDB

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/history", tags=["History"])

# ── Pydantic request/response schemas ────────────────────────────────────────

class HistoryCreateRequest(BaseModel):
    inputType: str = Field(..., description="Type of input scanned (e.g. SMS, WhatsApp, Call)")
    maskedInput: str = Field(..., description="The masked text that was analyzed")
    riskLevel: str = Field(..., description="High, Medium, Low, Safe")
    confidence: int = Field(..., description="Confidence score 0-100")
    scamType: str = Field(..., description="Label like OTP Fraud, Job Scam")
    summary: str = Field(..., description="Summary of analysis")
    redFlags: List[str] = Field(default_factory=list, description="Suspicious signs")
    suspiciousPhrases: List[str] = Field(default_factory=list, description="Extracted suspicious phrases")
    englishExplanation: str = Field(..., description="Explanation in English")
    urduExplanation: str = Field(..., description="Explanation in Roman Urdu")
    safeActions: List[str] = Field(default_factory=list, description="Recommended safe steps")
    doNotDo: List[str] = Field(default_factory=list, description="Things not to do")
    reportText: Optional[str] = Field(default=None, description="Nullable generated report")

class HistoryResponse(BaseModel):
    id: str
    createdAt: datetime
    inputType: str
    maskedInput: str
    riskLevel: str
    confidence: int
    scamType: str
    summary: str
    redFlags: List[str]
    suspiciousPhrases: List[str]
    englishExplanation: str
    urduExplanation: str
    safeActions: List[str]
    doNotDo: List[str]
    reportText: Optional[str] = None

# ── Helper converter ──────────────────────────────────────────────────────────

def to_response_model(db_record: ScanRecordDB) -> HistoryResponse:
    """Safely decode database fields stored as JSON strings back into lists."""
    try:
        red_flags = json.loads(db_record.redFlags) if db_record.redFlags else []
    except Exception:
        red_flags = []

    try:
        suspicious_phrases = json.loads(db_record.suspiciousPhrases) if db_record.suspiciousPhrases else []
    except Exception:
        suspicious_phrases = []

    try:
        safe_actions = json.loads(db_record.safeActions) if db_record.safeActions else []
    except Exception:
        safe_actions = []

    try:
        do_not_do = json.loads(db_record.doNotDo) if db_record.doNotDo else []
    except Exception:
        do_not_do = []

    return HistoryResponse(
        id=db_record.id,
        createdAt=db_record.createdAt,
        inputType=db_record.inputType,
        maskedInput=db_record.maskedInput,
        riskLevel=db_record.riskLevel,
        confidence=db_record.confidence,
        scamType=db_record.scamType,
        summary=db_record.summary,
        redFlags=red_flags,
        suspiciousPhrases=suspicious_phrases,
        englishExplanation=db_record.englishExplanation,
        urduExplanation=db_record.urduExplanation,
        safeActions=safe_actions,
        doNotDo=do_not_do,
        reportText=db_record.reportText
    )

# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("", response_model=HistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_history_record(
    payload: HistoryCreateRequest,
    session: Session = Depends(get_session)
):
    """
    POST /api/history
    Saves a scan record, converting list fields to JSON strings for database compatibility.
    Returns the decoded saved record.
    """
    try:
        db_record = ScanRecordDB(
            inputType=payload.inputType,
            maskedInput=payload.maskedInput,
            riskLevel=payload.riskLevel,
            confidence=payload.confidence,
            scamType=payload.scamType,
            summary=payload.summary,
            redFlags=json.dumps(payload.redFlags),
            suspiciousPhrases=json.dumps(payload.suspiciousPhrases),
            englishExplanation=payload.englishExplanation,
            urduExplanation=payload.urduExplanation,
            safeActions=json.dumps(payload.safeActions),
            doNotDo=json.dumps(payload.doNotDo),
            reportText=payload.reportText
        )
        saved = crud.save_scan(session, db_record)
        return to_response_model(saved)
    except Exception as e:
        logger.exception("Database transaction failed during create_history_record")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

@router.get("", response_model=List[HistoryResponse])
async def list_history_records(
    limit: int = 20,
    session: Session = Depends(get_session)
):
    """
    GET /api/history
    Fetches recent scan records ordered by createdAt descending.
    Decodes JSON strings back to actual lists in the response.
    """
    try:
        records = crud.get_recent_scans(session, limit=limit)
        return [to_response_model(r) for r in records]
    except Exception as e:
        logger.exception("Database query failed during list_history_records")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
