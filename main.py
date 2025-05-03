import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub

from dialogs import working_dialog, settings_dialog, routers
from keyboards.main_menu import main_menu
from settings import settings
from database import AsyncDBConnection
from services import DeleteMessageService, ObjectLoadService, CacheService
from clients import Logger, RabbitMqClient, RedisClient, S3Client
from middlewares import TrackMessageMiddleware, DBSessionMiddleware, RepositoriesInitMiddleware, I18nMiddleware
from background_tasks.tasks import listen_expired_keys_task
from utils.i18n import create_translator_hub

Logger().load_config()


async def main():
    s3 = S3Client(settings=settings)
    rabbit = RabbitMqClient(settings=settings, exchange=settings.rabbitmq.EXCHANGES.message_deleter)
    redis_client = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STATE_NUMBER)
    cache_client = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STORAGE_NUMBER)

    await cache_client.set_notify_keyspace_event
    await listen_expired_keys_task.kiq()

    dms = DeleteMessageService(broker=rabbit)
    obj_service = ObjectLoadService(obj_client=s3)
    cache_service = CacheService(storage=cache_client)

    state_storage = RedisStorage(redis=redis_client.redis, key_builder=DefaultKeyBuilder(with_destiny=True))
    db_session = AsyncDBConnection(settings=settings)
    translator: TranslatorHub = create_translator_hub()

    bot = Bot(settings.bot.TOKEN)
    dp = Dispatcher(bot=bot, storage=state_storage)
    dp.include_routers(*routers, working_dialog, settings_dialog)
    setup_dialogs(dp)

    dp.update.middleware(DBSessionMiddleware(await db_session.get_db()))
    dp.update.middleware(RepositoriesInitMiddleware())
    dp.message.middleware(TrackMessageMiddleware(process_service=dms))
    dp.message.middleware(I18nMiddleware())

    await main_menu(bot)
    await dp.start_polling(
        bot,
        cache_service=cache_service,
        msg_service=dms,
        obj_service=obj_service,
        _translator=translator
    )


if __name__ == "__main__":
    try:
        logging.info("Bot has started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot has stopped")
