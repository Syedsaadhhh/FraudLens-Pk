import requests
import json
import sys

# Force UTF-8 output to avoid Windows cp1252 terminal issues
sys.stdout.reconfigure(encoding='utf-8')

BASE = "http://localhost:8000"

print("=== STEP 1: Create a scan record ===")
post_resp = requests.post(f"{BASE}/api/history", json={
    "inputType": "SMS",
    "maskedInput": "Dear HBL customer, your OTP is 1234. Share now to avoid account block.",
    "riskLevel": "High",
    "confidence": 95,
    "scamType": "OTP Fraud",
    "summary": "Impersonates bank to steal OTP.",
    "redFlags": ["OTP request", "Urgent language", "Bank impersonation"],
    "suspiciousPhrases": ["Share now", "account block"],
    "englishExplanation": "This message is risky because it asks for OTP while threatening account suspension.",
    "urduExplanation": "Ye message khatarnak hai kyun ke ye OTP mang raha hai aur account band karne ki dhamki de raha hai.",
    "safeActions": ["Call HBL helpline 111-111-111", "Never share OTP"],
    "doNotDo": ["Do not share OTP", "Do not click any link"],
    "reportText": None
})
scan = post_resp.json()
scan_id = scan["id"]
print(f"Scan created. Status: {post_resp.status_code}  ID: {scan_id}")

print("\n=== STEP 2: Generate report via POST /api/report ===")
report_resp = requests.post(f"{BASE}/api/report", json={"id": scan_id})
print(f"Status: {report_resp.status_code}")
report_data = report_resp.json()
print(report_data["reportText"])

print("\n=== STEP 3: Verify reportText persisted in GET /api/history ===")
hist_resp = requests.get(f"{BASE}/api/history?limit=1")
records = hist_resp.json()
report_in_history = records[0]["reportText"] if records else None
if report_in_history:
    print(f"SAVED - first 100 chars: {report_in_history[:100]}")
else:
    print("MISSING - reportText not found in history!")

print("\n=== STEP 4: Test 404 for unknown ID ===")
bad_resp = requests.post(f"{BASE}/api/report", json={"id": "nonexistent-id-xyz"})
print(f"Status: {bad_resp.status_code}")
print(f"Detail: {bad_resp.json()['detail']}")

print("\n=== All tests complete! ===")
