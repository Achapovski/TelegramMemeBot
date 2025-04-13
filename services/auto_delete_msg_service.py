from typing import Unpack
from dataclasses import dataclass

from clients.RabbitMq import RabbitMqClient
from clients.Redis import RedisClient
from schemes import Settings, DeliveryDelMessageScheme


@dataclass
class DeleteMessageService:
    settings: Settings
    broker: RabbitMqClient
    storage: RedisClient

    async def delete_msg(self, chat_id: int, *message_ids: Unpack[tuple[int]]) -> int:
        if not message_ids:
            return 0

        message = DeliveryDelMessageScheme(chat_id=chat_id, message_ids=message_ids)
        await self.broker.publish_message(message)
        return len(message.message_ids)

    async def track_message(self, key: str | int, *values: Unpack[tuple[int]]):
        message = DeliveryDelMessageScheme(chat_id=key, message_ids=values)
        await self.broker.publish_message(message)
