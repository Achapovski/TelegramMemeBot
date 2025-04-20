import asyncio
import logging.config

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from fluentogram import TranslatorHub

from handlers import routers
from keyboards.main_menu import main_menu
from settings import settings
from database import AsyncDBConnection
from services import DeleteMessageService, ObjectLoadService
from clients import Logger, RabbitMqClient, RedisClient, S3Client
from middlewares import TrackMessageMiddleware, DBSessionMiddleware, RepositoriesInitMiddleware, I18nMiddleware
from utils.i18n import create_translator_hub

Logger().load_config()


async def main():
    state_storage = RedisClient(settings=settings, DB_NUMBER=settings.redis.DB_STATE_NUMBER)

    db_session = AsyncDBConnection(settings=settings)
    s3 = S3Client(settings=settings)
    rabbit = RabbitMqClient(settings=settings, exchange=settings.rabbitmq.EXCHANGES.message_deleter)

    dms = DeleteMessageService(broker=rabbit)
    obj_service = ObjectLoadService(obj_client=s3)

    bot = Bot(settings.bot.TOKEN)
    dp = Dispatcher(bot=bot, storage=RedisStorage(redis=state_storage.redis))

    dp.include_routers(*routers)

    translator: TranslatorHub = create_translator_hub()

    dp.update.middleware(DBSessionMiddleware(await db_session.get_db()))
    dp.update.middleware(RepositoriesInitMiddleware())
    dp.message.middleware(TrackMessageMiddleware(process_service=dms))
    dp.message.middleware(I18nMiddleware())

    await main_menu(bot)
    await dp.start_polling(bot, obj_repo=s3, msg_service=dms, obj_service=obj_service, _translator=translator)


if __name__ == "__main__":
    try:
        logging.info("Bot has started")
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot has stopped")
