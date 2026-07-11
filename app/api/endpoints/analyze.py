from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List

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
    # Check if the input is empty or only whitespace
    if not payload.text or not payload.text.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty."
        )
    
    # Return fixed dummy JSON response as requested
    return {
        "riskLevel": "High",
        "confidence": 92,
        "scamType": "OTP Fraud",
        "summary": "This message is likely trying to steal OTP.",
        "redFlags": ["OTP request", "Urgent language", "Suspicious link"],
        "englishExplanation": "This message is risky because it asks for OTP or private details.",
        "urduExplanation": "Ye message risky hai kyun ke ye OTP ya private details mang raha hai.",
        "safeActions": ["Do not share OTP", "Open official app manually"],
        "doNotDo": ["Do not click unknown link", "Do not send money"]
    }
