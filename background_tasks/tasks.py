import json

from background_tasks.dependencies import Dependency
from clients import RedisClient, BackgroundTaskClient
from schemes.models.users import UserSettingsDTO
from settings import settings
from custom_types import ShadowKey


broker = BackgroundTaskClient(
    redis=RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STATE_NUMBER)
).broker


# TODO: Дополнить способ удаление shadow ключа после получения данных
@broker.task()
async def listen_expired_keys_task():
    redis = await Dependency.clients.get_redis()
    pubsub = redis.redis.pubsub()
    settings_repo = await Dependency.repositories.user_settings

    await pubsub.psubscribe("__keyevent@1__:expired")

    async for message in pubsub.listen():
        if message["type"] == "pmessage" and not ShadowKey.from_str(user_id := message["data"]):
            settings_schema = await redis.get_value(ShadowKey(message["data"]).to_str())
            data = json.loads(settings_schema)
            user_settings = UserSettingsDTO.model_validate({"id": user_id, **data})

            await settings_repo.update_user_settings(
                user_id=int(user_id), language=user_settings.language_locale, dialog_type=user_settings.dialog_type
            )
