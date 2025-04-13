import json

from clients.Redis import RedisClient
from settings import settings


async def message_id_write(key: str, *values):
    redis = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STORAGE_NUMBER)
    data = await redis.get_value(key=key)

    # FIXME: отправлять команды в redis одним пулом
    if not data:
        await redis.set_value(key=key, value=values)
    else:
        result: list = json.loads(s=data)
        result.extend(values)
        await redis.set_value(key=key, value=result)
    data = json.loads(await redis.get_value(key=key))

    # FIXME: Вынести в отдельную функцию
    if len(data) > 8:
        await redis.set_value(key, value=[*reversed(data[-1:-8:-1])])
        return data[-8::-1]

    return []
