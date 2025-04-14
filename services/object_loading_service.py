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
        key = PrefixKey(key=key, prefix=unique_prefix)
        return await self.obj_client.upload_object(file=obj, key=key)

    async def download_object(self, key: str, unique_prefix: str) -> HttpUrl:
        obj_url = await self.obj_client.get_object_link(key=key, prefix=unique_prefix)
        return HttpUrl(url=obj_url)

    @staticmethod
    async def split_file_on_name_and_ext(file_name_with_ext: str) -> tuple[str, str]:
        file = Path(file_name_with_ext)
        return file.stem, file.suffix
