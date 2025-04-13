from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import BinaryIO
from urllib.parse import quote
from collections import namedtuple

from aiobotocore.session import get_session, AioSession

from schemes import Settings
from schemes.storages import S3ResponseScheme

PrefixKey = namedtuple("PrefixKey", "key prefix")


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

    async def upload_object(self, file: BinaryIO, file_name: str, prefix: str,
                            file_extension: str = "", **kwargs) -> PrefixKey:
        key = f"{prefix}/{file_name}" + f".{file_extension}" if file_extension else file_extension

        async with self.get_client() as client:
            await client.put_object(Bucket=self.bucket, Key=key, Body=file)

        return PrefixKey(*key.split("/"))

    async def get_object(self, key: str, prefix: str):
        async with self.get_client() as client:
            return await client.get_object(Bucket=self.bucket, Key=self._get_full_key_name(key=key, prefix=prefix))

    async def get_object_from_public_container(self, key: str, prefix: str):
        full_key = self._get_full_key_name(key=key, prefix=prefix)
        return quote(string=fr"https://43ec0fd9-e13c-4fed-a8c9-1d615f3b69a8.selstorage.ru/{full_key}", safe=":/")

    async def get_object_link(self, key: str, prefix: str):
        return f"{self.config["endpoint_url"]}/{self.bucket}/{self._get_full_key_name(key=key, prefix=prefix)}"

    async def get_all_objects(self, prefix: str):
        async with self.get_client() as client:
            response = await client.list_objects_v2(Bucket=self.bucket, Prefix=prefix)
            # for obj in S3ResponseScheme.model_validate(response).contents:
            #     print(f"Found object: {obj.key}, {obj.last_modified}")
            # print("Empty")
            return [obj.key for obj in S3ResponseScheme.model_validate(response).contents]

    async def download_all_objects(self, keys: list[str]):
        async with self.get_client() as client:
            result = [self.get_object(item) for item in keys]

    @staticmethod
    def _get_full_key_name(key: str, prefix: str):
        return f"{prefix}/{key}"
