import logging
from functools import lru_cache, wraps
from inspect import signature
from typing import Any, Coroutine, Callable

from aiogram_dialog import DialogManager


class DialogDataKwargsDecorator:
    def __init__(
            self,
            *elements,
            middleware_: bool = True,
            start_: bool = True,
            global_: bool = False,
            checking_: bool = True
    ):
        self.elements: tuple = elements
        self._middleware_data: bool = middleware_
        self._start_data: bool = start_
        self._global: bool = global_
        self._checking = checking_
        self.__middleware_data_property = "middleware_data"
        self.__start_data_property = "start_data"

    @lru_cache()
    def __call__(self, func: Callable[..., Coroutine]):
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Callable[..., Coroutine]:
            dialog_manager = self._find_dialog_manager(args, kwargs)
            _extra_data = self._find_args_in_data(dialog_manager=dialog_manager)
            _extra_data.update(kwargs)
            valid_params = self._check_signature(func, kwargs=_extra_data)

            return await func(*args, **valid_params)
        return wrapper

    def _find_args_in_data(self, dialog_manager: DialogManager) -> dict[str, Any]:
        extra_kwargs: dict[str, Any] = {}

        for element in self.elements:
            if self._start_data and (arg := dialog_manager.start_data.get(element)):
                extra_kwargs[element] = arg
            if self._middleware_data and (arg := dialog_manager.middleware_data.get(element)):
                extra_kwargs[element] = arg
            if self._global and (managed_radio := dialog_manager.find(element)):
                extra_kwargs[element] = managed_radio.get_checked() if self._checking else managed_radio
        return extra_kwargs

    def _find_dialog_manager(self, args, kwargs) -> DialogManager | None:
        if kwargs.get("dialog_manager"):
            return kwargs["dialog_manager"]

        for arg in args:
            if hasattr(arg, self.__middleware_data_property) and hasattr(arg, self.__start_data_property):
                return arg

        return logging.error("DialogManager not found on decorated function")

    @staticmethod
    def _check_signature(func: Callable[..., Coroutine], kwargs: dict[str, Any]) -> dict:
        arguments, result_kwargs = signature(func).parameters.items(), {}

        for name, type_ in arguments:
            if name in kwargs:
                result_kwargs[name] = kwargs[name]

        return result_kwargs
