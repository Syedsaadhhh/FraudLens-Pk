import logging
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from sqlmodel import Session

from app.db import crud
from app.db.database import get_session
from app.services.report_builder import build_report_text

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/report", tags=["Report"])


class ReportRequest(BaseModel):
    id: str


class ReportResponse(BaseModel):
    id: str
    reportText: str


@router.post("", response_model=ReportResponse, status_code=status.HTTP_200_OK)
async def generate_report(
    payload: ReportRequest,
    session: Session = Depends(get_session),
):
    """
    POST /api/report
    Looks up a scan by ID, generates a formatted plain-text report,
    saves it to the record's reportText field, and returns it.
    """
    if not payload.id or not payload.id.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Request body must include a non-empty 'id' field."
        )

    record = crud.get_scan_by_id(session, payload.id.strip())
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No scan record found with id '{payload.id}'. "
                   "Use GET /api/history to retrieve valid scan IDs."
        )

    try:
        report_text = build_report_text(record)
        crud.update_report_text(session, payload.id.strip(), report_text)
        logger.info(f"Report generated and saved for scan id: {payload.id}")
        return ReportResponse(id=record.id, reportText=report_text)
    except Exception as e:
        logger.exception(f"Failed to generate report for scan id: {payload.id}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {str(e)}"
        )
