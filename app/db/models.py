from sqlalchemy import Column, Integer, String, JSON, Float, DateTime, func
from .base import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

class ModelMetadata(Base):
    __tablename__ = "model_metadata"

    id = Column(Integer, primary_key=True, index=True)
    model_id = Column(String(36), index=True, nullable=False)
    seo_title = Column(String(100), nullable=True)
    market_description = Column(String, nullable=True)
    tags = Column(JSON, nullable=True)
    vertices = Column(Integer, nullable=True)
    polygons = Column(Integer, nullable=True)
    file_size_kb = Column(Float, nullable=True)
    complexity_score = Column(Float, nullable=True)
    estimated_time_minutes = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
