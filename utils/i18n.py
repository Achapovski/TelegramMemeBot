import os
from pathlib import Path

from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub

from custom_types.enums import LocalesEnum


def find_locales(
        locale: LocalesEnum,
        locales_dir: str = "locales",
        messages_dir: str = "LC_MESSAGES"
) -> FluentTranslator:
    filenames = os.scandir(locales_dir + os.sep + locale.name + os.sep + messages_dir)
    locale_files = [loc.path for loc in filenames if Path(loc).suffix == ".ftl"]

    return FluentTranslator(
        locale=locale.name,
        translator=FluentBundle.from_files(
            locale=locale.value,
            filenames=locale_files
        )
    )


def create_translator_hub() -> TranslatorHub:
    translator_hub = TranslatorHub(
        locales_map={
            LocalesEnum.ru.name: (LocalesEnum.ru.name, LocalesEnum.en.name),
            LocalesEnum.en.name: (LocalesEnum.en.name, LocalesEnum.ru.name)
        },
        translators=[find_locales(locale=locale) for locale in LocalesEnum]
    )
    return translator_hub
