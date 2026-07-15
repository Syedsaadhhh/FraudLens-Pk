"""
test_history.py — FraudLens PK

Tests the POST and GET endpoints for the history router.
"""

import urllib.request
import urllib.error
import json

URL = "http://127.0.0.1:8000/api/history"

def test_post_history():
    print("\nTesting POST /api/history...")
    payload = {
        "inputType": "SMS",
        "maskedInput": "Dear HBL customer, OTP is 1234...",
        "riskLevel": "High",
        "confidence": 95,
        "scamType": "OTP Fraud",
        "summary": "Impersonates bank asking for OTP.",
        "redFlags": ["OTP request", "Urgent language"],
        "suspiciousPhrases": ["reactivate HBL account"],
        "englishExplanation": "Risky because it asks for OTP.",
        "urduExplanation": "Ye message risky hai kyun ke ye OTP mang raha hai.",
        "safeActions": ["Call bank helpline directly"],
        "doNotDo": ["Do not share OTP", "Do not click link"]
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            print(f"Status Code: {status}")
            print("Response Body (Saved Record):")
            print(json.dumps(parsed, indent=2))
            assert status == 201
            assert "id" in parsed
            assert parsed["riskLevel"] == "High"
            # Verify list fields are actual JSON arrays (not strings)
            assert isinstance(parsed["redFlags"], list)
            assert isinstance(parsed["suspiciousPhrases"], list)
            print("POST /api/history test passed!\n")
            return parsed["id"]
    except Exception as e:
        print(f"POST test failed: {e}")
        if hasattr(e, 'read'):
            print("Error details:", e.read().decode("utf-8"))
        raise

def test_get_history():
    print("Testing GET /api/history...")
    req = urllib.request.Request(
        f"{URL}?limit=5",
        method="GET"
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            body = response.read().decode("utf-8")
            parsed = json.loads(body)
            print(f"Status Code: {status}")
            print(f"Retrieved {len(parsed)} recent records.")
            print("First Record Details:")
            if len(parsed) > 0:
                print(json.dumps(parsed[0], indent=2))
                assert isinstance(parsed[0]["redFlags"], list)
                assert isinstance(parsed[0]["suspiciousPhrases"], list)
            assert status == 200
            print("GET /api/history test passed!\n")
    except Exception as e:
        print(f"GET test failed: {e}")
        raise

if __name__ == "__main__":
    print("Starting history integration tests...")
    record_id = test_post_history()
    test_get_history()
    print("All history integration tests PASSED!")
