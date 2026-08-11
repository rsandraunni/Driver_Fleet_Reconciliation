from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.config.settings import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True
)


# Create database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False
)


# Base class for all database models
class Base(DeclarativeBase):
    pass


# Dependency for FastAPI and other services
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()