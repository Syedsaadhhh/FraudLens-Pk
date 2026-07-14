# FraudLens PK — AI Digital Scam Shield for Pakistan

A hackathon frontend project that helps users detect online scams before they click, pay, or share
sensitive information. Frontend only — no backend, dummy data throughout.

## Tech Stack

- Next.js (App Router)
- React
- Tailwind CSS
- shadcn/ui-style components
- Lucide React icons
- Framer Motion
- Recharts (dashboard chart)

## Getting Started

```bash
npm install
npm run dev
```

Then open **http://localhost:3000** in your browser.

## Project Structure

```
app/
  page.js              -> Landing page ("/")
  analyze/page.js       -> Analyzer page ("/analyze")
  dashboard/page.js     -> Dashboard page ("/dashboard")
  layout.js             -> Root layout (shared HTML shell)
  globals.css           -> Tailwind + global styles
  icon.svg               -> Favicon

components/
  ui/                   -> Reusable primitives (Button, Badge, Card, Textarea)
  shared/               -> Navbar, Footer, small shared bits
  landing/               -> Landing page sections (Hero, Stats, Features, ...)
  analyzer/              -> Analyzer form + result cards
  dashboard/              -> Dashboard widgets (stats, table, chart, tip)

data/
  dummyData.js           -> All dummy content (stats, scam types, history rows, etc.)

lib/
  analyzeText.js          -> Rule-based "AI" analyzer (keyword matching, no backend)
  styleHelpers.js          -> Shared Tailwind class helpers
  useCountUp.js            -> Count-up animation hook
  utils.js                 -> cn() class-merging helper
```

## How the Analyzer Works (no backend)

`lib/analyzeText.js` scans whatever text you paste for keywords tied to common Pakistani
scam patterns (OTP fraud, bank phishing, fake jobs, parcel scams, prize scams, payment scams,
investment scams, QR scams, malware links, impersonation). It always returns a complete result:
risk score, risk level, scam type, confidence, red flags, English + Roman Urdu explanations,
safe actions, and a "do not" list — even for random text, which falls back to a low-risk result.

## Scripts

- `npm run dev` — start the local dev server
- `npm run build` — production build
- `npm run start` — run the production build
- `npm run lint` — run ESLint

## Repository

https://github.com/Syedsaadhhh/FraudLens-Pk
