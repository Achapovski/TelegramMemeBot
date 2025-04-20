import logging
from typing import Unpack
from dataclasses import dataclass

from aiormq.exceptions import PublishError, ConnectionChannelError
from clients.RabbitMq import RabbitMqClient
from schemes import DeliveryDelMessageScheme


@dataclass
class DeleteMessageService:
    broker: RabbitMqClient

    async def track_message(self, key: str | int, *values: Unpack[tuple[int]]):
        message = DeliveryDelMessageScheme(chat_id=key, message_ids=values)
        try:
            await self.broker.publish_message(message)
        except (PublishError, ConnectionChannelError) as err:
            logging.critical("%s connection error. %s" % (self.broker.__class__.__name__, err))
