from dataclasses import dataclass, field

from custom_types.enums import ObjectType
from custom_types.messages import CustomMessageUpdate
from schemes.types.types import FileMeta


@dataclass
class PrefixKey:
    key: str
    prefix: str
    _separator: str = field(default="/")

    def __repr__(self):
        return f"{self.prefix}{self._separator}{self.key}"

    def to_str(self):
        return self.__repr__()


__all__ = [
    "ObjectType",
    "CustomMessageUpdate",
    "PrefixKey",
    "FileMeta"
]
