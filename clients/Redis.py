import json
import logging
from dataclasses import dataclass
from typing import Union

import redis.asyncio as redis
from redis.exceptions import ConnectionError
from redis.asyncio.client import Pipeline

from schemes import Settings
from utils.predicates import is_json

RedisValueType = Union[str, int, dict, list, tuple]


@dataclass
class RedisClient:
    settings: Settings
    DB_NUMBER: int
    DECODE_RESPONSE: bool = True

    def __post_init__(self):
        self.host: str = self.settings.redis.HOST
        self.port: int = self.settings.redis.PORT
        self.db: int = self.DB_NUMBER
        self.dsn: str = self.settings.redis.dsn(self.db).unicode_string()
        self._decode_response: bool = self.DECODE_RESPONSE
        self._pipeline: Pipeline | None = None

    @property
    def redis(self) -> redis.client.Redis:
        try:
            return redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=self._decode_response)
        except ConnectionError as err:
            logging.critical("Redis connection error.")
            raise err

    @property
    async def set_notify_keyspace_event(self) -> None:
        return await self.redis.config_set(name="notify-keyspace-events", value="Ex")

    async def set_value(self, key: str, value: RedisValueType, ex: int = None) -> RedisValueType:
        data = json.dumps(value)
        await self.pipeline()
        await self.redis.set(name=key, value=data, ex=ex)
        data = await self.get_value(key=key)
        await self.pipeline_execute()
        return data

    async def get_value(self, key: str) -> RedisValueType:
        data = await self.redis.get(key)
        if is_json(data):
            return json.loads(s=data)
        return data

    async def get_all_values(self) -> dict[str, str]:
        data = {}
        for key in await self.get_keys():
            data[key] = await self.get_value(key=key)
        return data

    async def get_keys(self) -> list[str]:
        return await self.redis.keys()

    async def del_value(self, key: str) -> None:
        return await self.redis.delete(key)

    async def del_all_values(self) -> None:
        if not (values := await self.get_all_values()):
            logging.debug("No values for deleting")
            return
        return await self.redis.delete(*values)

    async def get_ttl(self, key) -> int:
        return await self.redis.ttl(name=key)

    async def pipeline(self) -> Pipeline:
        self._pipeline = await self.redis.pipeline()
        return self._pipeline

    async def pipeline_execute(self) -> Pipeline.execute:
        return await self._pipeline.execute()
