import sys
import os
import pytest
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Ensure project root is on sys.path so "app" package is found
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.models.base import Base
from app.db import get_db
from app.main import app

# Use in-memory SQLite shared across connections for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # keeps the same in-memory DB for all sessions
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    """Create all tables once for the entire test session."""
    Base.metadata.create_all(bind=engine)
    yield
    # Tables exist only in memory; no teardown needed.


@pytest.fixture(scope="function")
def db_session():
    """Provide a fresh SQLAlchemy session and override FastAPI get_db per test."""
    session = TestingSessionLocal()

    def override_get_db():
        try:
            yield session
        finally:
            # session will be closed after the test, not during request
            pass

    app.dependency_overrides[get_db] = override_get_db
    yield session
    session.close()
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def event_loop():
    """Create a new event loop per test function (needed for asyncio plugins)."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
