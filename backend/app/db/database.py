import logging
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel
from app.core.config import settings

logger = logging.getLogger(__name__)

# Validate that DATABASE_URL is configured
database_url = settings.DATABASE_URL
if not database_url:
    logger.error("DATABASE_URL environment variable is missing or empty.")
    raise ValueError("DATABASE_URL environment variable is not set.")

# Adjust database URL if it uses postgresql:// instead of postgresql+psycopg2:// or postgresql+psycopg://
# SQLAlchemy 1.4+ deprecated plain postgresql:// for some dialects, but psycopg2 is the standard.
# Since we have both psycopg (psycopg3) and psycopg2 installed, both are supported.
# Let's keep the user's config value directly.
engine = create_engine(
    database_url,
    echo=False,  # Set to True if we want to log SQL queries
    pool_pre_ping=True  # Check connection health before executing queries
)

def init_db() -> None:
    """Initialize database tables defined in SQLModel metadata."""
    try:
        logger.info("Initializing database tables...")
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise

def get_session() -> Generator[Session, None, None]:
    """Dependency generator for retrieving db sessions in FastAPI endpoints."""
    with Session(engine) as session:
        yield session
