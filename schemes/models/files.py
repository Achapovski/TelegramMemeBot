from pydantic import BaseModel, HttpUrl, Field

from custom_types import ObjectType


class FileCreateCheme(BaseModel):
    url: str | HttpUrl
    owner_id: int
    title: str = Field(max_length=50, min_length=1)
    type: ObjectType


class FileDTO(FileCreateCheme):
    id: int
