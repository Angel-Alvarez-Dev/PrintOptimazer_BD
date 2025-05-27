# app/api/ai.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

@router.get("/status")
async def ai_status():
    """Health endpoint for AI router"""
    return {"status": "ai router operational"}