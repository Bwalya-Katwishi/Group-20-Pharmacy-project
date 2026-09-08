import os
import tempfile
from pathlib import Path

_db = Path(tempfile.gettempdir()) / "apoza_pytest.db"
if _db.exists():
    _db.unlink()
os.environ["DATABASE_URL"] = f"sqlite:///{_db.as_posix()}"
os.environ["SEED_ON_START"] = "false"
os.environ["SECRET_KEY"] = "pytest-secret"

import pytest
from fastapi.testclient import TestClient

from apoza.main import create_app
from apoza.persistence.database import SessionLocal, engine
from apoza.persistence.seed import seed_if_empty
from apoza.persistence.tables import Base


@pytest.fixture
def db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    seed_if_empty(session)
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    app = create_app()
    with TestClient(app) as c:
        yield c
