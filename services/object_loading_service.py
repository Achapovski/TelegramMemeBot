import io
from dataclasses import dataclass
from pathlib import Path
from typing import BinaryIO

from pydantic import HttpUrl

from clients.S3 import S3Client
from custom_types import PrefixKey


@dataclass
class ObjectLoadService:
    obj_client: S3Client

    async def upload_object(self, key: str, unique_prefix: str, obj: BinaryIO) -> PrefixKey:
        self.check_file_path(key)
        key = PrefixKey(key=key, prefix=unique_prefix)
        return await self.obj_client.upload_object(file=obj, key=key)

    async def get_object_url(self, key: str, unique_prefix: str) -> HttpUrl:
        self.check_file_path(key)
        key = PrefixKey(key=key, prefix=unique_prefix)
        obj_url = await self.obj_client.get_object_url(key=key)
        return HttpUrl(url=obj_url)

    @staticmethod
    def check_file_path(file_path: str) -> None:
        path = Path(file_path)
        if not (path.stem and path.suffix):
            raise ValueError("Incorrect filepath or file extension")
