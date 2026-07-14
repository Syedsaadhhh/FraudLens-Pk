from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

from app.services import ai_service

router = APIRouter()

class AnalyzeRequest(BaseModel):
    text: str = Field(default="", description="The message or text content to analyze for fraud/scam.")

class AnalyzeResponse(BaseModel):
    riskLevel: str
    confidence: int
    scamType: str
    summary: str
    redFlags: List[str]
    englishExplanation: str
    urduExplanation: str
    safeActions: List[str]
    doNotDo: List[str]

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_message(payload: AnalyzeRequest):
    # Validate input is not empty
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty."
        )

    # Delegate to AI service — returns structured dict or raises HTTPException
    result = await ai_service.analyze_text(payload.text.strip())
    return result
