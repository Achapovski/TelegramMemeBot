import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from clients.RabbitMq import RabbitMqClient
from clients.Redis import RedisClient
from handlers import routers
from clients.S3 import S3Client
from keyboards.main_menu import main_menu
from middlewares.track_msg import TrackMessageMiddleware
from settings import settings
from database import AsyncDBConnection
from services.auto_delete_msg_service import DeleteMessageService
from middlewares.storage import DBSessionMiddleware, RepositoriesInitMiddleware


async def main():
    state_storage = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STATE_NUMBER)
    cache_storage = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STORAGE_NUMBER)

    db_session = AsyncDBConnection(settings=settings)
    s3 = S3Client(settings=settings)
    rabbit = RabbitMqClient(settings=settings, exchange=settings.rabbitmq.EXCHANGES.message_deleter)

    dms = DeleteMessageService(settings=settings, storage=cache_storage, broker=rabbit)
    bot = Bot(settings.bot.TOKEN)
    dp = Dispatcher(bot=bot, storage=RedisStorage(redis=state_storage.redis))

    dp.include_routers(*routers)

    dp.update.middleware(DBSessionMiddleware(await db_session.get_db()))
    dp.update.middleware(RepositoriesInitMiddleware())
    dp.message.middleware(TrackMessageMiddleware(process_service=dms))

    await main_menu(bot)
    await dp.start_polling(bot, obj_repo=s3, cache_repo=cache_storage, msg_service=dms)


if __name__ == "__main__":
    try:
        print("Bot has started")
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped.")
