from dataclasses import dataclass

from custom_types import ShadowKey
from clients import RedisClient


@dataclass
class CacheService:
    storage: RedisClient
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    async def to_cache(self, key: str | int, value: str, exp_time: int = 40, shadow: bool = False):
        print(await self.storage.get_keys())
        if shadow:
            await self._set_shadow_key(original_key=key, value=value, exp_time=exp_time)
            await self.storage.set_value(key=key.__str__(), value="", ex=exp_time)
        else:
            await self.storage.set_value(key=key.__str__(), value=value, ex=exp_time)
        print("Cached")

    async def from_cache(self, key: str | int, shadow: bool = False) -> str | None:
        if shadow:
            return await self.storage.get_value(key=self._build_shadow_key(original_key=key))
        return await self.storage.get_value(key=key.__str__())

    async def callback_if_expired(self, callback, **kwargs):
        await callback.kiq(**kwargs)

    async def _set_shadow_key(self, original_key: str | int, value: str, exp_time: int, time_coefficient: int = 1.5):
        shadow_key = self._build_shadow_key(original_key=original_key)
        await self.storage.set_value(key=shadow_key, value=value, ex=int(exp_time*time_coefficient))

    def _build_shadow_key(self, original_key: int | str) -> str:
        return ShadowKey(key=original_key).to_str()
