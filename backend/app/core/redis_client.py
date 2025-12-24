import redis
import json
from typing import Optional, Any
from app.core.config import settings


class RedisClient:
    def __init__(self):
        self.redis = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True,
            encoding="utf-8"
        )

    async def get(self, key: str) -> Optional[Any]:
        """Get value from Redis"""
        try:
            value = self.redis.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None

    async def set(self, key: str, value: Any, expire: int = 3600) -> bool:
        """Set value in Redis with expiration"""
        try:
            self.redis.setex(
                key,
                expire,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False

    async def delete(self, key: str) -> bool:
        """Delete key from Redis"""
        try:
            self.redis.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False

    async def exists(self, key: str) -> bool:
        """Check if key exists in Redis"""
        try:
            return self.redis.exists(key) > 0
        except Exception as e:
            print(f"Redis exists error: {e}")
            return False


redis_client = RedisClient()
