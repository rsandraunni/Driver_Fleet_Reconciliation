'''
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config.settings import settings
from app.models.base import Base


@pytest.fixture
def db():
    engine = create_engine(
        settings.TEST_DATABASE_URL,
        pool_pre_ping=True,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    # Create tables in the test database
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()
'''

import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models so SQLAlchemy registers all tables
import app.models

from app.config.settings import settings
from app.models.base import Base


@pytest.fixture
def db():
    engine = create_engine(
        settings.TEST_DATABASE_URL,
        pool_pre_ping=True,
    )

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    # Create all tables in the test database
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()

        # Remove tables after the test
        Base.metadata.drop_all(bind=engine)

        engine.dispose()