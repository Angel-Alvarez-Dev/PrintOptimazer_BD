# tests/test_ai_endpoints.py

import pytest
from fastapi.testclient import TestClient
from celery import Celery
from app.api.main import app
from app.core.config import settings
from app.db.base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import ModelMetadata

# Fixture: in-memory DB and override SessionLocal and app dependency
@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr("app.api.deps.SessionLocal", TestingSessionLocal)
    monkeypatch.setattr("app.db.session.SessionLocal", TestingSessionLocal)
    return TestingSessionLocal

# Fixture: TestClient
@pytest.fixture
def client():
    return TestClient(app)

# Fixture: Celery in eager mode and stub AsyncResult
@pytest.fixture(autouse=True)
def celery_eager(monkeypatch):
    celery_app = Celery(broker="memory://", backend="rpc://")
    celery_app.conf.task_always_eager = True
    # Stub AsyncResult to use actual task results
    monkeypatch.setattr("app.core.celery.celery_app", celery_app)
    return celery_app

def test_enqueue_and_get_result_flow(client, in_memory_db):
    # Enqueue SEO title
    resp = client.post("/api/v1/ai/seo/testmodel")
    assert resp.status_code == 200
    data = resp.json()
    task_id = data["task_id"]
    assert data["status"] == "queued"

    # Check pending state
    resp2 = client.get(f"/api/v1/ai/result/{task_id}")
    assert resp2.status_code == 200
    assert resp2.json()["status"] in ("PENDING", "STARTED", "SUCCESS")

def test_result_success_returns_data(client, in_memory_db, monkeypatch):
    # Pre-insert metadata for SUCCESS state
    session = in_memory_db()
    meta = ModelMetadata(
        model_id="foo",
        seo_title="A",
        market_description="B",
        tags=["x"],
        vertices=1, polygons=2,
        file_size_kb=0.5, complexity_score=0.1,
        estimated_time_minutes=5.0,
        task_id="tok123"
    )
    session.add(meta)
    session.commit()

    # Stub AsyncResult to return SUCCESS
    class FakeResult:
        state = "SUCCESS"
        result = None
    monkeypatch.setattr("app.api.ai.celery_app.AsyncResult", lambda tid: FakeResult())

    resp = client.get("/api/v1/ai/result/tok123")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "SUCCESS"
    assert payload["data"]["seo_title"] == "A"
    assert payload["data"]["estimated_time_minutes"] == 5.0

def test_result_failure_returns_error(client, in_memory_db, monkeypatch):
    # Stub AsyncResult to return FAILURE
    class FakeResultFail:
        state = "FAILURE"
        result = Exception("boom")
    monkeypatch.setattr("app.api.ai.celery_app.AsyncResult", lambda tid: FakeResultFail())

    resp = client.get("/api/v1/ai/result/anything")
    assert resp.status_code == 200
    payload = resp.json()
    assert payload["status"] == "FAILURE"
    assert "boom" in payload["error"]
