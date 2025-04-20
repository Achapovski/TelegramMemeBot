from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import BinaryIO
from urllib.parse import quote

from aiobotocore.session import get_session, AioSession

from custom_types import PrefixKey
from schemes import Settings
from schemes.storages import S3ResponseScheme


@dataclass
class S3Client:
    settings: Settings

    def __post_init__(self):
        self.config = {
            "aws_access_key_id": self.settings.s3.ACCESS_KEY.get_secret_value(),
            "aws_secret_access_key": self.settings.s3.SECRET_KEY.get_secret_value(),
            "endpoint_url": str(self.settings.s3.ENDPOINT_URL),
        }
        self.bucket = self.settings.s3.BUCKET
        self.service_name = "s3"
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self) -> AioSession:
        async with self.session.create_client(
                service_name=self.service_name, **self.config
        ) as client:
            yield client

    async def upload_object(self, file: BinaryIO, key: PrefixKey) -> PrefixKey:
        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket, Key=key.to_str(), Body=file)
        return key

    async def download_object(self, key: str, prefix: str):
        async with self.get_client() as client:
            return await client.download_object(Bucket=self.bucket, Key=PrefixKey(key=key, prefix=prefix).to_str())

    @staticmethod
    async def get_object_url(key: PrefixKey):
        # FIXME: Необходимо заменить на реализацию на основе приватного контейнера
        return quote(string=fr"https://43ec0fd9-e13c-4fed-a8c9-1d615f3b69a8.selstorage.ru/{key.to_str()}", safe=":/")

    async def get_object_link(self, key: PrefixKey):
        return f"{self.config["endpoint_url"]}/{self.bucket}/{key.to_str()}"

    async def get_all_objects(self, prefix: str) -> list[str]:
        async with self.get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            return [obj.key for obj in S3ResponseScheme.model_validate(response).contents]

    async def download_all_objects(self, prefix: str) -> list:
        obj_names = await self.get_all_objects(prefix=prefix)
        return [await self.download_object(prefix=prefix, key=key) for key in obj_names]
