from fastapi import APIRouter
from app.core.redis import redis_client

router = APIRouter(tags=["health"])

@router.get("/health")
async def health():
    # Check Redis
    try:
        await redis_client.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "error"
    return {"status": "ok", "redis": redis_status}