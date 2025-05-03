import functools
import asyncio


def auto_commit_decorator(func):
    """Декоратор, который после вызова метода автоматически выполняет commit."""

    @functools.wraps(func)
    async def wrapper(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)
        # Если у экземпляра есть session и флаг не выключен, вызываем commit.
        # Флаг будет установлен через альтернативный декоратор.
        if not getattr(wrapper, "_disable_auto_commit", False):
            if hasattr(self, "session"):
                await self.session.commit()
        return result

    return wrapper


def disable_auto_commit(func):
    """Декоратор, который помечает метод как не требующий автоматического commit."""
    func._disable_auto_commit = True
    return func


def decorate_all_methods(cls):
    for attr_name in dir(cls):
        # Пропускаем dunder-методы
        if attr_name.startswith("__"):
            continue
        attr = getattr(cls, attr_name)
        # Проверяем, является ли атрибут вызываемым и асинхронной функцией
        if callable(attr) and asyncio.iscoroutinefunction(attr):
            # Если метод помечен как не требующий auto_commit, пропускаем его
            if getattr(attr, "_disable_auto_commit", False):
                continue
            # Оборачиваем функцию в auto_commit_decorator
            decorated = auto_commit_decorator(attr)
            setattr(cls, attr_name, decorated)
    return cls


@decorate_all_methods
class Repository:
    def __init__(self, session):
        self.session = session  # session должен быть AsyncSession

    async def set_params(self, params: dict):
        """Метод, который выполняет insert и после завершения автоматически делает commit."""
        print("Вставляем данные:", params)
        # Здесь выполнение запроса, например:
        await self.session.execute(
            "INSERT INTO table (params) VALUES (:params)",
            {"params": params}
        )
        return params

    @disable_auto_commit
    async def get_data(self, id: int):
        """Метод, не требующий автоматического commit (только чтение)."""
        print("Извлекаем данные для id:", id)
        result = await self.session.execute(
            "SELECT * FROM table WHERE id = :id",
            {"id": id}
        )
        return result.fetchall()
