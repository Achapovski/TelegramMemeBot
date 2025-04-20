import logging
from dataclasses import dataclass

import aiormq
from aiormq.exceptions import AMQPException, ConnectionChannelError, ChannelNotFoundEntity

from schemes import Settings
from schemes.settings import BasicRabbitExchange
from schemes.brokers.messages import DeliveryMessageScheme


@dataclass
class RabbitMqClient:
    settings: Settings
    exchange: BasicRabbitExchange

    async def get_broker_connection(self) -> aiormq.abc.AbstractConnection:
        return await aiormq.connect(url=str(self.settings.rabbitmq.AMQP_DSN))

    async def get_broker_channel(self) -> aiormq.abc.AbstractChannel:
        connection = await self.get_broker_connection()
        try:
            return await connection.channel()
        except (ConnectionChannelError, AMQPException) as err:
            logging.critical("Channel creation error. %s" % err)

    async def declare_exchanger(self) -> aiormq.abc.Exchange.DeclareOk:
        channel = await self.get_broker_channel()
        return await channel.exchange_declare(
            exchange=self.exchange.name,
            exchange_type=self.exchange.type
        )

    async def publish_message(self, message: DeliveryMessageScheme):
        channel = await self.get_broker_channel()
        await channel.basic_publish(
            body=message.model_dump_json().encode(),
            exchange=self.exchange.name
        )
