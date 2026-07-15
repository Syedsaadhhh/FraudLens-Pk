from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.api import api_router
from app.core.config import settings
from app.db.database import init_db
from app.routers import history

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Enable CORS for frontend/backend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include api router with prefix /api
app.include_router(api_router, prefix=settings.API_V1_STR)
# Include history router (prefix /api/history is defined inside the router)
app.include_router(history.router)

import threading

@app.on_event("startup")
def on_startup():
    try:
        init_db()
    except Exception as e:
        print("\n" + "="*80)
        print("DATABASE INIT ERROR: Failed to connect or initialize the PostgreSQL database.")
        print(f"DATABASE_URL: {settings.DATABASE_URL}")
        print("Please check that:")
        print("  1. PostgreSQL is running locally or at the specified host.")
        print("  2. The database named 'fraudlens' exists.")
        print("  3. Your username and password in .env are correct.")
        print(f"Detailed Error: {e}")
        print("="*80 + "\n")
        # Still raise the error to let uvicorn report startup failure cleanly and exit
        raise

@app.get("/")
def root():
    return {
        "message": "Welcome to FraudLens PK Backend API. Use /api/analyze for analysis, or go to /docs for interactive Swagger UI documentation."
    }
