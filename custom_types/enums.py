from enum import Enum


class Typer:
    def __new__(cls, value: str):
        return type(value.title(), (str,), {})(value)


class ObjectType(Enum):
    voice = Typer("voice")
    video = Typer("video")
    video_note = Typer("video_note")
    document = Typer("document")
    photo = Typer("photo")
    text = Typer("text")
    undefined = Typer("undefined")

    def __repr__(self):
        return self.value


class LocalesEnum(Enum):
    ru = "ru-RU"
    en = "en-US"

    def __str__(self):
        return self.name
