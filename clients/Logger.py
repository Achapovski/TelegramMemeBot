import logging
import logging.config
import os
from functools import lru_cache
from pathlib import Path
from sys import stderr
from typing import Literal
from io import TextIOWrapper

from yaml import safe_load


class Logger:
    """
    Initialize logger config if file logging_config.yml exists,
    in otherwise load default config with initialization params. Can`t init more than once.
    """

    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(
            self,
            log_level: Literal["NOTSET", "INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL"],
            logger_name: str,
            filemode: Literal["a", "w"] = "a",
            config_file: str = None,
            filename: str = None,
            stream: TextIOWrapper = None,
            date_format: str = None,
            file_config_name: str = None
    ):
        self.log_level = log_level
        self.filemode = filemode
        self.encoding = "utf-8"
        self.stream = (stderr, stream)[bool(stream)]
        self.file_name = ("logs/logs.log", filename)[bool(filename)]
        self.config_file = ("logging_config.yml", config_file)[bool(config_file)]
        self.date_format = ("%Y-%m-%d %H:%M:%S", date_format)[bool(date_format)]
        self.format = ("[%(asctime)s]: [%(module)s] [(func name: %(funcName)s, line %(lineno)d)]"
                       " #%(levelname)s: %(name)s - %(message)s")
        self.file_config_name = Path(file_config_name if file_config_name else "")
        self.logger = self.get_logger(logger_name)
        self._default_file_config_name = Path("logging_config.yml")
        self.load_logging_config(file_config_name=self.file_config_name)

    def init_base_config(self):
        return logging.basicConfig(
            level=self.log_level,
            encoding=self.encoding,
            format=self.format,
            datefmt=self.date_format,
            handlers=[self.get_file_handler(), self.get_stderr_handler()],
        )

    def get_file_handler(self, file_name: str = None):
        file_name = (self.file_name, file_name)[bool(file_name)]
        return logging.FileHandler(encoding=self.encoding, filename=file_name, mode=self.filemode)

    def get_stderr_handler(self):
        return logging.StreamHandler(stream=self.stream)

    @lru_cache(maxsize=1)
    def load_logging_config(self, file_config_name: Path | None) -> None:
        if file_config_name and self._is_file_config_exist(self.file_config_name):
            return logging.config.dictConfig(
                config=self.read_logging_config_file(config_file=file_config_name)
            )

        if self._is_file_config_exist(self._default_file_config_name):
            return logging.config.dictConfig(
                config=self.read_logging_config_file(config_file=self._default_file_config_name)
            )

        self.init_base_config()

    @staticmethod
    def get_logger(name: str):
        return logging.getLogger(name)

    @staticmethod
    def read_logging_config_file(config_file: Path) -> dict:
        with open(config_file.name) as log_config:
            log_config = safe_load(stream=log_config)
        return log_config

    @staticmethod
    def _is_valid_config_file_name(file_name: Path | None) -> bool:
        return file_name.suffix == ".yml" and file_name.stem

    @lru_cache(maxsize=1)
    def _is_file_config_exist(self, file_name: Path) -> bool:
        self._is_valid_config_file_name(file_name=file_name)

        for file in os.scandir():
            if file_name.name == file.name:
                return True
        return False
