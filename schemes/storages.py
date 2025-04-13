from datetime import datetime

from pydantic import BaseModel, Field


class S3ObjectScheme(BaseModel):
    key: str = Field(alias="Key")
    last_modified: datetime = Field(alias="LastModified")


class S3ResponseScheme(BaseModel):
    contents: list[S3ObjectScheme] = Field(alias="Contents", default_factory=list)
