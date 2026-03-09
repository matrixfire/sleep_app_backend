import redis

from app.core.config import settings


def get_redis() -> redis.Redis:
    return redis.Redis(**settings.redis_kwargs())

