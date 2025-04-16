from mimetypes import guess_type

from aiogram.types import InlineQueryResultVoice, InlineQueryResultArticle, InlineQueryResultUnion, \
    InputTextMessageContent, InlineQueryResultDocument, InlineQueryResultVideo, InlineQueryResultPhoto

from custom_types import ObjectType
from schemes import FileDTO
from multipledispatch import dispatch

from utils.loaders import is_valid_mime_type


def build_result_list(objects_list: list[FileDTO]) -> list[InlineQueryResultUnion]:
    articles = []
    for idx, element in enumerate(objects_list, 1):
        articles.append(DispatchedInlineQueryResult(
            obj=element,
            element_id=idx
        ).get_query_result(
            getattr(ObjectType, element.type.value).value
        ))
    articles.sort(key=lambda x: (str(x.type), x.title), reverse=True)
    return articles


class DispatchedInlineQueryResult:
    def __init__(self, obj: FileDTO, element_id: int):
        self.obj = obj
        self.element_id = str(element_id)

    @dispatch(type(ObjectType.voice.value))
    def get_query_result(self, value):
        return InlineQueryResultVoice(
            voice_url=self.obj.url,
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.video.value))
    def get_query_result(self, value):
        return InlineQueryResultVideo(
            mime_type="video/mp4",
            video_url=self.obj.url,
            thumbnail_url=self.obj.url.replace(".mp4", ".PNG"),
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.video_note.value))
    def get_query_result(self, value):
        return InlineQueryResultVideo(
            mime_type="video/mp4",
            video_url=self.obj.url,
            thumbnail_url=self.obj.url.replace(".mp4", ".PNG"),
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.document.value))
    def get_query_result(self, value):
        return InlineQueryResultDocument(
            mime_type=self.document_mime_type,
            document_url=self.obj.url,
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.photo.value))
    def get_query_result(self, value):
        return InlineQueryResultPhoto(
            photo_url=self.obj.url,
            thumbnail_url=self.obj.url,
            description=self.obj.title,
            photo_width=200,
            photo_height=200,
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.text.value))
    def get_query_result(self, value):
        return InlineQueryResultArticle(
            input_message_content=InputTextMessageContent(message_text=self.obj.title),
            **self._get_id_title_data()
        )

    @dispatch(type(ObjectType.undefined.value))
    def get_query_result(self, value):
        print("Undefined type")
        return

    @property
    def document_mime_type(self):
        type_, encoding = guess_type(self.obj.url)
        if is_valid_mime_type(self.obj.url):
            return type_
        return "application/zip"

    def _get_id_title_data(self) -> dict[str, str]:
        return {"id": self.element_id, "title": self.obj.title}

