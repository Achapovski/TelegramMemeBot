from typing import Unpack
from dataclasses import dataclass

from clients.RabbitMq import RabbitMqClient
from schemes import DeliveryDelMessageScheme


@dataclass
class DeleteMessageService:
    broker: RabbitMqClient

    async def track_message(self, key: str | int, *values: Unpack[tuple[int]]):
        message = DeliveryDelMessageScheme(chat_id=key, message_ids=values)
        await self.broker.publish_message(message)
