# FraudLens PK — Demo Scam Cases

This file contains 5 real-world scam cases used for manual testing of the AI analysis endpoint.

---

## Case 1: OTP Fraud (Bank Impersonation)

**Message:**
```
Aap ka HBL account suspend ho gaya hai. Account ko reactivate karne ke liye apna OTP share karein: 0300-1234567. Ye OTP sirf 5 minutes ke liye valid hai. Forun reply karein warna account permanently band ho jayega.
```

**Expected Output:**
- `riskLevel`: High
- `scamType`: OTP Fraud / Bank Impersonation
- `redFlags`: OTP request, urgency, account suspension threat, phone number

---

## Case 2: Lucky Draw / Prize Fraud

**Message:**
```
Mubarak ho! Aap ne Jazz Lucky Draw mein 50,000 rupay jeete hain. Prize claim karne ke liye abhi apna CNIC number aur bank account details send karein WhatsApp pe: 0312-9876543. Offer sirf aaj ke liye hai!
```

**Expected Output:**
- `riskLevel`: High
- `scamType`: Lucky Draw Fraud
- `redFlags`: Unsolicited prize, CNIC request, bank details request, urgency, WhatsApp contact

---

## Case 3: Fake Job Offer

**Message:**
```
Urgent Hiring! Work from home opportunity. Earn 50,000-80,000 per month. No experience required. Send your CV and 2000 rupay registration fee to Jazz Cash number 0333-1122334. Limited seats available!
```

**Expected Output:**
- `riskLevel`: High
- `scamType`: Job Scam
- `redFlags`: Registration fee, too-good-to-be-true salary, JazzCash payment request, urgency

---

## Case 4: Investment / Ponzi Scheme

**Message:**
```
Crypto investment opportunity! Invest 10,000 aur 30 din mein 50,000 hasil karein. 100% guaranteed return. Hamari company registered hai. Abhi WhatsApp karein: 0345-5678901. Hazar logon ne pehle se fayda utha liya!
```

**Expected Output:**
- `riskLevel`: High
- `scamType`: Investment Fraud
- `redFlags`: Guaranteed returns, unrealistic profit, urgency, WhatsApp-only contact, social proof manipulation

---

## Case 5: Safe / Legitimate Message (Negative Test)

**Message:**
```
Dear customer, your UBL bank statement for June 2025 is ready. Please log in to your UBL Digital app or visit www.ubldigital.com to download it. For help, call 111-825-888.
```

**Expected Output:**
- `riskLevel`: Low or Safe
- `scamType`: Safe Message
- `redFlags`: (empty or minimal)
- Note: No OTP request, official domain, official helpline number

---

## How to Test

1. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Open Swagger UI at `http://127.0.0.1:8000/docs`

3. POST each message above to `/api/analyze` and verify the response contains all 9 required fields.

4. Run the automated test suite:
   ```bash
   python test_api.py
   ```
