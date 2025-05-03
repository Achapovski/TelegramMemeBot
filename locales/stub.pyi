from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    message: Message
    object: Object
    settings: Settings
    buttons: Buttons


class Message:
    @staticmethod
    def welcome() -> Literal["""Ты можешь отослать мне голосовое или видео сообщение и я запомню его."""]: ...


class Object:
    @staticmethod
    def valid() -> Literal["""Отлично! Теперь придумай название для своего мема."""]: ...

    @staticmethod
    def invalid() -> Literal["""Я не могу распознать тип твоего сообщения :(
Используй голосовое или видео сообщение."""]: ...

    @staticmethod
    def need_title() -> Literal["""Теперь придумай название для своего мема."""]: ...

    @staticmethod
    def created() -> Literal["""Отлично, мем создан."""]: ...

    @staticmethod
    def not_created() -> Literal["""Что-то пошло не так, скорее всего ошибка на моей стороне."""]: ...


class Settings:
    labels: SettingsLabels

    @staticmethod
    def locale_type() -> Literal["""Язык"""]: ...

    @staticmethod
    def dialog_type() -> Literal["""Диалог"""]: ...


class SettingsLabels:
    @staticmethod
    def settings() -> Literal["""Настройки."""]: ...

    @staticmethod
    def dialog_type() -> Literal["""Сменить тип ведения диалога."""]: ...

    @staticmethod
    def locale_type() -> Literal["""Сменить язык."""]: ...


class Buttons:
    @staticmethod
    def confirm() -> Literal["""Подтвердить"""]: ...

