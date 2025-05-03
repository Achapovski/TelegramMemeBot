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


@dataclass
class ShadowKey:
    key: str
    _prefix: str = field(default="shdw")
    _separator: str = field(default=":")

    def __repr__(self):
        return f"{self._prefix}{self._separator}{self.key}"

    def to_str(self):
        return self.__repr__()

    @staticmethod
    def from_str(key: str, _prefix: str = "shdw", _separator: str = ":"):
        # FIXME: Написать регулярное выражение для парсинга строки и создания нового объекта
        splitted_key = key.split(_separator)
        if len(splitted_key) == 2 and splitted_key[0] == _prefix:
            return ShadowKey(key.split(_separator)[-1])
        return False


__all__ = [
    "ObjectType",
    "CustomMessageUpdate",
    "PrefixKey",
    "ShadowKey",
    "FileMeta"
]
