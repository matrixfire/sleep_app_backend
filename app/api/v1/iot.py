from __future__ import annotations

from typing import Any, Dict

from fastapi import APIRouter

from db.redis_client import get_redis

router = APIRouter(prefix="/iot", tags=["iot"])

QUEUE_KEY = "iot:sleep_data"


@router.post("/ingest")
def ingest_device_data(payload: Dict[str, Any]) -> dict[str, str]:
    """
    MVP IoT ingest endpoint.
    Fast path: push raw payload into Redis list and return 200 quickly.
    """
    r = get_redis()
    r.lpush(QUEUE_KEY, payload)
    return {"status": "queued"}

