# tests/test_ai_tasks.py

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from celery import Celery

from app.core.config import settings
from app.db.base import Base
from app.db.models import ModelMetadata
from app.tasks.ai_tasks import (
    generate_seo_title_task,
    generate_market_description_task,
    generate_tags_task,
    analyze_complexity_task,
    predict_print_time_task,
)
from app.services.ai_service import AIService, AIServiceError
from app.schemas.ai_task import PrintTimeRequest, ComplexityReport

# Fixture: in-memory SQLite and SessionLocal override
@pytest.fixture(autouse=True)
def in_memory_db(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr("app.tasks.ai_tasks.SessionLocal", TestingSessionLocal)
    return TestingSessionLocal

# Fixture: Celery eager mode
@pytest.fixture(autouse=True)
def celery_eager(monkeypatch):
    celery_app = Celery(broker="memory://", backend="rpc://")
    celery_app.conf.task_always_eager = True
    monkeypatch.setattr("app.tasks.ai_tasks.celery_app", celery_app)
    return celery_app

# Stub AIService methods to return deterministic values
class StubService(AIService):
    def generate_seo_title(self, model_id):
        return "Stub Title"
    def generate_market_description(self, model_id):
        return "Stub Description"
    def generate_tags(self, model_id):
        return ["tag1", "tag2"]
    def analyze_complexity(self, url):
        return ComplexityReport(vertices=10, polygons=20, file_size_kb=1.5, complexity_score=0.75)
    def predict_print_time(self, req):
        return PrintTimeRequest.model_validate({"model_file_url":req.model_file_url, "material":req.material, "layer_height_mm":req.layer_height_mm, "infill_percent":req.infill_percent})

@pytest.fixture(autouse=True)
def stub_ai_service(monkeypatch):
    monkeypatch.setattr("app.tasks.ai_tasks.AIService", StubService)

def test_generate_seo_title_persists(in_memory_db):
    model_id = "model1"
    generate_seo_title_task(model_id)
    db = in_memory_db()
    meta = db.query(ModelMetadata).filter_by(model_id=model_id).one()
    assert meta.seo_title == "Stub Title"

def test_generate_market_description_persists(in_memory_db):
    model_id = "model2"
    generate_market_description_task(model_id)
    db = in_memory_db()
    meta = db.query(ModelMetadata).filter_by(model_id=model_id).one()
    assert meta.market_description == "Stub Description"

def test_generate_tags_persists(in_memory_db):
    model_id = "model3"
    generate_tags_task(model_id)
    db = in_memory_db()
    meta = db.query(ModelMetadata).filter_by(model_id=model_id).one()
    assert meta.tags == ["tag1", "tag2"]

def test_analyze_complexity_persists(in_memory_db):
    model_id = "model4"
    analyze_complexity_task("http://example.com/model.stl", model_id)
    db = in_memory_db()
    meta = db.query(ModelMetadata).filter_by(model_id=model_id).one()
    assert meta.vertices == 10
    assert meta.polygons == 20
    assert meta.file_size_kb == 1.5
    assert meta.complexity_score == 0.75

def test_predict_print_time_persists(in_memory_db):
    model_id = "model5"
    req = {"model_file_url": "http://ex.com/m.stl", "material": "PLA", "layer_height_mm": 0.2, "infill_percent": 20}
    predict_print_time_task(req, model_id)
    db = in_memory_db()
    meta = db.query(ModelMetadata).filter_by(model_id=model_id).one()
    # Using stub, we expect attributes from the request
    assert meta.estimated_time_minutes == pytest.approx(req["infill_percent"])  # adjust as per stub logic
