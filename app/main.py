from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.redis import redis_client
from app.core.chroma import chroma_client
from app.routers import health

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify Redis and Chroma are reachable
    try:
        await redis_client.ping()
        print("Redis connected")
    except Exception as e:
        print(f"Redis connection failed: {e}")
    # Chroma doesn't have a simple ping; we'll just print that it's initialized
    print(f"Chroma initialized at {settings.chroma_persist_dir}")
    yield
    # Shutdown: close Redis connection
    await redis_client.aclose()
    print("Redis closed")

app = FastAPI(
    title="Support Agent API",
    version="0.1.0",
    description="Conversational support agent with memory and retrieval",
    lifespan=lifespan,
)

app.include_router(health.router)

@app.get("/")
async def root():
    return {"message": "Support Agent is running"}