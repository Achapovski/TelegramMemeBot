from dataclasses import dataclass
from functools import lru_cache

from taskiq_redis import RedisStreamBroker, RedisAsyncResultBackend

from clients import RedisClient


@dataclass
class BackgroundTaskClient:
    redis: RedisClient

    @property
    @lru_cache(maxsize=1)
    def broker(self) -> RedisStreamBroker:
        return RedisStreamBroker(url=self.redis.dsn).with_result_backend(result_backend=self.result_backend)

    @property
    @lru_cache(maxsize=1)
    def result_backend(self):
        return RedisAsyncResultBackend(redis_url=self.redis.dsn, keep_results=True)

    def __hash__(self):
        return hash(f"{self.redis.dsn}")
