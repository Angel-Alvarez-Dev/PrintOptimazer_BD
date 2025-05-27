# tests/test_health_ready.py
import pytest
from starlette.testclient import TestClient
import redis as _redis
from app.api.main import app
import app.db.session

@pytest.fixture
def client():
    return TestClient(app)

class DummyDB:
    def execute(self, query):
        return None

class DummyRedis:
    def ping(self):
        return True

@ pytest.mark.parametrize("db_error,redis_error,status_code", [
    (False, False, 200),
    (True, False, 503),
    (False, True, 503),
])
def test_ready_various(db_error, redis_error, status_code, monkeypatch, client):
    # Mock DB
    def fake_session():
        db = DummyDB()
        if db_error:
            def fail(q):
                raise Exception("DB fail")
            db.execute = fail
        return db
    monkeypatch.setattr(app.db.session, "SessionLocal", fake_session)

    # Mock Redis
    def fake_from_url(url):
        r = DummyRedis()
        if redis_error:
            def fail():
                raise Exception("Redis fail")
            r.ping = fail
        return r
    monkeypatch.setattr(_redis, "from_url", fake_from_url)

    response = client.get("/ready")
    assert response.status_code == status_code


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}