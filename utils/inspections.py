from typing import Union

from aiogram.types import Message, Voice, Document, Video, PhotoSize, VideoNote

from custom_types import ObjectType, FileMeta


def get_file_from_message(message: Message) -> FileMeta:
    if getattr(message, "voice") and (type_ := ObjectType.voice.value):
        file = _get_file_descriptor(message.voice)
    elif getattr(message, "video") and (type_ := ObjectType.video.value):
        file = _get_file_descriptor(message.video)
    elif getattr(message, "document") and (type_ := ObjectType.document.value):
        file = _get_file_descriptor(message.document)
    elif getattr(message, "photo") and (type_ := ObjectType.photo.value):
        file = _get_file_descriptor(message.photo)
    elif getattr(message, "video_note") and (type_ := ObjectType.video_note.value):
        file = _get_file_descriptor(message.video_note)
    else:
        file = message.text
        type_ = ObjectType.undefined

    return FileMeta(id=file, type=type_)


def _get_file_descriptor(telegram_file_type: Union[str, Voice, Document, Video, VideoNote, list[PhotoSize]]) -> str:
    if isinstance(telegram_file_type, list):
        return [element.file_id for element in telegram_file_type][-1]

    if getattr(telegram_file_type, "file_id"):
        return telegram_file_type.file_id

    return telegram_file_type
