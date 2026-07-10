# FraudLens PK

**AI Digital Scam Shield for Pakistan**

FraudLens PK is a hackathon MVP that helps Pakistani users check suspicious WhatsApp/SMS messages, URLs, emails, QR text, and screenshots. The app uses AI to detect scam type, risk level, red flags, Urdu/English explanation, safe actions, and a simple scan report.

## Core Demo Flow

```text
Suspicious message / URL / screenshot
        ↓
AI analysis
        ↓
Risk score + scam type
        ↓
Red flags + Urdu/English explanation
        ↓
Safe action checklist
        ↓
History / report
```

## MVP Features

- Scam message scanner
- URL risk checker
- AI risk scoring: Low / Medium / High
- Scam type detection: OTP fraud, fake job, parcel scam, payment scam, phishing, prize scam, investment scam
- Red flag highlights
- Urdu + English explanation
- Safe actions and do-not-do checklist
- Basic dashboard and scan history
- Optional screenshot OCR and report export if time allows

## Tech Stack

- Frontend: Next.js + Tailwind CSS + shadcn/ui
- Backend: Next.js API Routes
- AI: Gemini or OpenAI API
- Database: Supabase/Firebase or local mock data first
- OCR: Tesseract.js or OCR API, optional
- Deployment: Vercel

## Team Roles

- **Saad:** Product direction, scam logic, AI prompts, demo flow, pitch, final QA
- **Maryam:** Frontend UI, landing page, analyzer UI, dashboard UI, documentation, submission sheet
- **Mohsin:** Backend API, AI integration, database/history, Vercel deployment

## Build Rule

Do not overbuild. First make the main flow work perfectly:

```text
Paste message → Analyze → Risk score → Scam type → Red flags → Urdu/English explanation → Safe actions
```

After this works, then add dashboard, history, OCR, and report export.
