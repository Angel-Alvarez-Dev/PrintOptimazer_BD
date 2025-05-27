# app/api/main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
import redis
import logging.config

from app.core.config import settings
from app.core.logging_config import LOGGING_CONFIG
from app.api.deps import get_db
from app.api.ai import router as ai_router

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)

app = FastAPI(title="PrintOptimizer BD API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include AI router
app.include_router(ai_router)

# Health check
@app.get("/health")
async def health():
    return {"status": "ok"}

# Readiness check: DB and Redis
@app.get("/ready")
async def ready(db=Depends(get_db)):
    try:
        db.execute("SELECT 1")
    except Exception:
        raise HTTPException(status_code=503, detail="Database not ready")
    try:
        r = redis.from_url(settings.REDIS_URL)
        r.ping()
    except Exception:
        raise HTTPException(status_code=503, detail="Redis not ready")
    return {"status": "ready"}

# Metrics endpoint for Prometheus
@app.get("/metrics")
async def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)