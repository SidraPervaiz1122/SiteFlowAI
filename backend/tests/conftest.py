import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.app.database import Base, get_db
from backend.app.main import app
from backend.db.seed import seed_database
from fastapi.testclient import TestClient

TEST_DB_URL = "sqlite:///./backend/storage/test_siteflow.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    seed_database(reset=True)
    yield

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def contractor_token(client):
    res = client.post("/api/auth/quick-switch", json={"role": "CONTRACTOR"})
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture
def re_token(client):
    res = client.post("/api/auth/quick-switch", json={"role": "RE"})
    assert res.status_code == 200
    return res.json()["access_token"]

@pytest.fixture
def client_token(client):
    res = client.post("/api/auth/quick-switch", json={"role": "CLIENT"})
    assert res.status_code == 200
    return res.json()["access_token"]
