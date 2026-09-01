import json
from typing import List, Dict
from app.core.redis import redis_client

def _key(session_id: str) -> str:
    return f"chat:{session_id}"

async def get_history(session_id: str) -> List[Dict[str, str]]:
    raw = await redis_client.get(_key(session_id))
    if not raw:
        return []
    return json.loads(raw)

async def add_message(session_id: str, role: str, content: str):
    history = await get_history(session_id)
    history.append({"role": role, "content": content})
    await redis_client.set(_key(session_id), json.dumps(history))