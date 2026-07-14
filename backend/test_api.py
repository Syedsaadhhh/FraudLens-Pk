"""
test_api.py — FraudLens PK

Integration tests for the /api/analyze endpoint.
Tests 5 real Pakistani scam cases from docs/DEMO_SCAM_CASES.md
plus one empty-input validation test.

Usage: python test_api.py  (requires server running on localhost:8000)
"""

import urllib.request
import urllib.error
import json

BASE_URL = "http://127.0.0.1:8000/api/analyze"

REQUIRED_FIELDS = [
    "riskLevel", "confidence", "scamType", "summary",
    "redFlags", "englishExplanation", "urduExplanation",
    "safeActions", "doNotDo"
]

# ── Test cases from docs/DEMO_SCAM_CASES.md ──────────────────────────────────

SCAM_CASES = [
    {
        "name": "Case 1 — OTP Fraud / Bank Impersonation",
        "text": (
            "Aap ka HBL account suspend ho gaya hai. Account ko reactivate karne ke liye "
            "apna OTP share karein: 0300-1234567. Ye OTP sirf 5 minutes ke liye valid hai. "
            "Forun reply karein warna account permanently band ho jayega."
        ),
        "expect_high_risk": True,
    },
    {
        "name": "Case 2 — Lucky Draw Fraud",
        "text": (
            "Mubarak ho! Aap ne Jazz Lucky Draw mein 50,000 rupay jeete hain. "
            "Prize claim karne ke liye abhi apna CNIC number aur bank account details "
            "send karein WhatsApp pe: 0312-9876543. Offer sirf aaj ke liye hai!"
        ),
        "expect_high_risk": True,
    },
    {
        "name": "Case 3 — Fake Job Offer",
        "text": (
            "Urgent Hiring! Work from home opportunity. Earn 50,000-80,000 per month. "
            "No experience required. Send your CV and 2000 rupay registration fee to "
            "Jazz Cash number 0333-1122334. Limited seats available!"
        ),
        "expect_high_risk": True,
    },
    {
        "name": "Case 4 — Investment / Ponzi Scheme",
        "text": (
            "Crypto investment opportunity! Invest 10,000 aur 30 din mein 50,000 hasil karein. "
            "100% guaranteed return. Hamari company registered hai. Abhi WhatsApp karein: "
            "0345-5678901. Hazar logon ne pehle se fayda utha liya!"
        ),
        "expect_high_risk": True,
    },
    {
        "name": "Case 5 — Safe / Legitimate Message",
        "text": (
            "Dear customer, your UBL bank statement for June 2025 is ready. "
            "Please log in to your UBL Digital app or visit www.ubldigital.com to download it. "
            "For help, call 111-825-888."
        ),
        "expect_high_risk": False,
    },
]


# ── Helper ────────────────────────────────────────────────────────────────────

def post_analyze(text: str):
    """POST to /api/analyze and return (status_code, parsed_body)."""
    data = json.dumps({"text": text}).encode("utf-8")
    req = urllib.request.Request(
        BASE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as response:
            return response.getcode(), json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8"))


def assert_all_fields(body: dict, case_name: str):
    """Assert all 9 required fields are present."""
    missing = [f for f in REQUIRED_FIELDS if f not in body]
    if missing:
        print(f"  ❌ FAILED — missing fields: {missing}")
        return False
    print(f"  ✅ All 9 fields present")
    return True


# ── Test runner ───────────────────────────────────────────────────────────────

def run_scam_tests():
    passed = 0
    failed = 0

    for case in SCAM_CASES:
        print(f"\n{'='*60}")
        print(f"Testing: {case['name']}")
        print(f"Input: {case['text'][:80]}...")

        status_code, body = post_analyze(case["text"])

        if status_code != 200:
            print(f"  ❌ FAILED — HTTP {status_code}: {body}")
            failed += 1
            continue

        ok = assert_all_fields(body, case["name"])
        if not ok:
            failed += 1
            continue

        risk = body.get("riskLevel", "")
        confidence = body.get("confidence", 0)
        scam_type = body.get("scamType", "")

        print(f"  riskLevel   : {risk}")
        print(f"  confidence  : {confidence}%")
        print(f"  scamType    : {scam_type}")
        print(f"  summary     : {body.get('summary', '')[:100]}")
        print(f"  redFlags    : {body.get('redFlags', [])}")

        passed += 1

    return passed, failed


def test_empty_input():
    print(f"\n{'='*60}")
    print("Testing: Empty input validation")
    status_code, body = post_analyze("")
    if status_code == 400 and "detail" in body:
        print(f"  ✅ Correct 400 error: {body['detail']}")
        return True
    else:
        print(f"  ❌ FAILED — expected 400, got {status_code}: {body}")
        return False


if __name__ == "__main__":
    print("FraudLens PK — API Integration Tests")
    print("Requires: uvicorn app.main:app --reload (running on localhost:8000)")

    passed, failed = run_scam_tests()
    empty_ok = test_empty_input()

    print(f"\n{'='*60}")
    print(f"RESULTS: {passed}/5 scam cases passed | Empty input test: {'✅' if empty_ok else '❌'}")
    if failed == 0 and empty_ok:
        print("✅ ALL TESTS PASSED")
    else:
        print(f"❌ {failed} test(s) failed")
