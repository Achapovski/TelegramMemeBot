import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from clients.Logger import Logger
from clients.RabbitMq import RabbitMqClient
from clients.Redis import RedisClient
from clients.S3 import S3Client
from handlers import routers
from keyboards.main_menu import main_menu
from settings import settings
from database import AsyncDBConnection
from services import DeleteMessageService, ObjectLoadService

from middlewares.track_msg import TrackMessageMiddleware
from middlewares.storage import DBSessionMiddleware, RepositoriesInitMiddleware


async def main():
    logger = Logger(log_level="INFO", file_config_name="config_.yml", logger_name=__name__)
    logger.logger.error("WARNING")

    state_storage = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STATE_NUMBER)
    cache_storage = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STORAGE_NUMBER)

    db_session = AsyncDBConnection(settings=settings)
    s3 = S3Client(settings=settings)
    rabbit = RabbitMqClient(settings=settings, exchange=settings.rabbitmq.EXCHANGES.message_deleter)

    dms = DeleteMessageService(broker=rabbit)
    obj_service = ObjectLoadService(obj_client=s3)

    bot = Bot(settings.bot.TOKEN)
    dp = Dispatcher(bot=bot, storage=RedisStorage(redis=state_storage.redis))

    dp.include_routers(*routers)

    dp.update.middleware(DBSessionMiddleware(await db_session.get_db()))
    dp.update.middleware(RepositoriesInitMiddleware())
    dp.message.middleware(TrackMessageMiddleware(process_service=dms))

    await main_menu(bot)
    await dp.start_polling(bot, obj_repo=s3, cache_repo=cache_storage, msg_service=dms, obj_service=obj_service)


if __name__ == "__main__":
    try:
        print("Bot has started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped.")
