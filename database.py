from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# --------------------------------------------------------
# Load environment variables
# --------------------------------------------------------
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL is missing in your .env file.")


# --------------------------------------------------------
# SQLAlchemy Engine (Optimized for Neon)
# --------------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,        # prevents stale connections
    pool_size=5,               # limit connections (Neon requirement)
    max_overflow=2,            # allow slight surge
    pool_timeout=30,           # wait for connection before failing
    echo=False                 # set to True for debug
)


# --------------------------------------------------------
# SessionLocal for FastAPI
# --------------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# --------------------------------------------------------
# Declarative Base
# --------------------------------------------------------
Base = declarative_base()


# --------------------------------------------------------
# FastAPI Dependency
# --------------------------------------------------------
def get_db():
    """
    Create a new database session for each request.
    Closes automatically to prevent connection leaks.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
