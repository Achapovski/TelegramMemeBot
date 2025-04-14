from pydantic import BaseModel, ConfigDict

from custom_types import ObjectType


class FileMeta(BaseModel):
    id: str
    type: ObjectType

    model_config = ConfigDict(use_enum_values=True)
