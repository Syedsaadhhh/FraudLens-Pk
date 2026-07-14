"""
ai_service.py — FraudLens PK

Handles all communication with the Google Gemini AI model.
Uses the modern `google-genai` SDK (2025) with Pydantic schema for
structured JSON output, ensuring the response always matches our contract.

Docs reference: https://ai.google.dev/gemini-api/docs/structured-output
"""

import json
import logging
from typing import List

from fastapi import HTTPException, status
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

from app.core.config import settings

logger = logging.getLogger(__name__)

# ── Pydantic schema — forces Gemini to return exactly this shape ──────────────

class ScamAnalysisResult(BaseModel):
    riskLevel: str = Field(description="One of: High, Medium, Low, Safe")
    confidence: int = Field(description="Confidence score 0-100")
    scamType: str = Field(description="Short label e.g. OTP Fraud, Job Scam, Safe Message")
    summary: str = Field(description="1-2 sentence plain English summary")
    redFlags: List[str] = Field(description="List of specific suspicious elements found")
    englishExplanation: str = Field(description="Detailed English explanation")
    urduExplanation: str = Field(description="Same explanation in Roman Urdu")
    safeActions: List[str] = Field(description="What the user SHOULD do")
    doNotDo: List[str] = Field(description="What the user must NEVER do")


# ── System prompt (loaded inline — mirrors docs/AI_PROMPT.md) ─────────────────

SYSTEM_PROMPT = """You are FraudLens PK, an expert AI fraud detection assistant for Pakistani users.
Your job is to analyze messages, SMS, WhatsApp texts, emails, or call scripts and determine if they are scams or fraudulent.

You have deep knowledge of scam patterns common in Pakistan, including:
- OTP (One-Time Password) theft
- Bank account impersonation (HBL, UBL, Meezan, MCB, Allied Bank, etc.)
- Mobile wallet scams (JazzCash, EasyPaisa)
- Fake job offers
- Lucky draw / prize fraud
- Investment and Ponzi schemes
- Loan app fraud
- SIM swap scams
- Phishing links (bit.ly, tinyurl, fake bank domains)
- WhatsApp account hijacking

CRITICAL RULES:
1. Respond with ONLY valid JSON matching the required schema. No markdown fences, no explanation.
2. The urduExplanation must be in Roman Urdu (Urdu written in English alphabet), not Arabic script.
3. riskLevel must be exactly one of: High, Medium, Low, Safe.
4. confidence must be an integer between 0 and 100.
5. redFlags, safeActions, and doNotDo must be non-empty arrays of strings.

Analyze the following message:"""


# ── Gemini client factory ─────────────────────────────────────────────────────

def _get_client() -> genai.Client:
    """Create and return a configured Gemini client."""
    api_key = settings.GEMINI_API_KEY
    if not api_key or api_key == "your_gemini_api_key_here":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="GEMINI_API_KEY is not configured. Add it to your .env file."
        )
    return genai.Client(api_key=api_key)


# ── Main analysis function ────────────────────────────────────────────────────

async def analyze_text(user_text: str) -> dict:
    """
    Send the user's message to Gemini and return a structured scam analysis.

    Uses Pydantic schema + response_mime_type='application/json' to force
    the model to return valid, schema-conformant JSON every time.

    Raises:
        HTTPException 503: If API key is missing.
        HTTPException 500: If Gemini call fails or response cannot be parsed.
    """
    client = _get_client()

    prompt = f"{SYSTEM_PROMPT}\n\n{user_text}"

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ScamAnalysisResult,
                temperature=0.2,   # Low temperature = more deterministic, consistent JSON
                max_output_tokens=1024,
            ),
        )

        raw_text = response.text
        logger.info("Gemini raw response: %s", raw_text[:200])

        # Parse the JSON safely
        parsed = json.loads(raw_text)

        # Validate all required fields are present
        required_fields = [
            "riskLevel", "confidence", "scamType", "summary",
            "redFlags", "englishExplanation", "urduExplanation",
            "safeActions", "doNotDo"
        ]
        missing = [f for f in required_fields if f not in parsed]
        if missing:
            logger.error("Gemini response missing fields: %s", missing)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"AI response was missing required fields: {missing}"
            )

        # Ensure types are correct (coerce confidence to int just in case)
        parsed["confidence"] = int(parsed.get("confidence", 0))

        return parsed

    except HTTPException:
        # Re-raise our own HTTP exceptions
        raise

    except json.JSONDecodeError as e:
        logger.error("Failed to parse Gemini JSON response: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI returned invalid JSON. Please try again. Error: {str(e)}"
        )

    except Exception as e:
        logger.error("Gemini API call failed: %s", str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI service error: {str(e)}"
        )
