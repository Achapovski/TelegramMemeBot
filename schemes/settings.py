from typing import Literal

from pydantic import BaseModel, SecretStr, Field, PostgresDsn, HttpUrl, AmqpDsn


class Bot(BaseModel):
    TOKEN: str


class DataBase(BaseModel):
    CONNECTION: str
    USER: str
    PASSWORD: SecretStr
    HOST: str
    PORT: int = Field(ge=1000, le=16394)
    DATABASE: str
    IS_ECHO: bool
    DSN: PostgresDsn


class Redis(BaseModel):
    HOST: str
    PORT: int = Field(ge=1000, le=16394)
    DB_DEFAULT_NUMBER: int = Field(ge=0, le=15)
    DB_STORAGE_NUMBER: int = Field(ge=0, le=15)
    DB_STATE_NUMBER: int = Field(ge=0, le=15)


class RabbitMQ(BaseModel):
    HOST: str
    PORT: int = Field(ge=1000, le=16394)
    LOGIN: str
    PASSWORD: SecretStr
    AMQP_DSN: AmqpDsn
    EXCHANGES: "RabbitExchange"
    QUEUES: "RabbitQueue"


class S3(BaseModel):
    ACCESS_KEY: SecretStr
    SECRET_KEY: SecretStr
    ENDPOINT_URL: HttpUrl
    BUCKET: str


class Settings(BaseModel):
    bot: Bot
    db: DataBase
    redis: Redis
    rabbitmq: RabbitMQ
    s3: S3


class BasicRabbitExchange(BaseModel):
    name: str
    type: Literal["direct", "topic", "fanout"]


class BasicRabbitQueue(BaseModel):
    name: str


class RabbitExchange(BaseModel):
    message_deleter: BasicRabbitExchange


class RabbitQueue(BaseModel):
    message_deleter: BasicRabbitQueue
