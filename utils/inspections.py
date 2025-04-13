from typing import Union

from aiogram.types import Message, Voice, Document, Video, PhotoSize, VideoNote

from custom_types import ObjectType


def get_file_from_message(message: Message) -> dict[str, Union[str, Voice, Document, Video]] | None:
    data = {"file": message.text, "file_extension": True}

    match message:
        case _ if getattr(message, "voice") and (type_ := ObjectType.voice.value):
            data["file"] = _get_file_descriptor(message.voice)
        case _ if getattr(message, "video") and (type_ := ObjectType.video.value):
            data["file"] = _get_file_descriptor(message.video)
        case _ if getattr(message, "document") and (type_ := ObjectType.document.value):
            data["file"] = _get_file_descriptor(message.document)
        case _ if getattr(message, "photo") and (type_ := ObjectType.photo.value):
            data["file"] = _get_file_descriptor(message.photo)
        case _ if getattr(message, "video_note") and (type_ := ObjectType.video_note.value):
            data["file"] = _get_file_descriptor(message.video_note)
        case _ if getattr(message, "text") and (type_ := ObjectType.text.value):
            data.pop("file_extension")
        case _ if type_ := ObjectType.undefined.value:
            pass

    data.update({"type": type_})
    return data


def _get_file_descriptor(telegram_file_type: Union[str, Voice, Document, Video, VideoNote, list[PhotoSize]]) -> str:
    if isinstance(telegram_file_type, list):
        # FIXME: Выбрать одну размерность фотографий
        return [element.file_id for element in telegram_file_type][2]

    if getattr(telegram_file_type, "file_id"):
        return telegram_file_type.file_id

    return telegram_file_type
