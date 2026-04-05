from typing import Any, Callable, TypeVar

from sqlalchemy import inspect

T = TypeVar("T")


def _map_relation(orm: Any, relation_name: str, mapper: Callable[[Any], T]) -> list[T]:
    """
    Безопасно маппит отношение: если не загружено — возвращает пустой список.
    """
    try:
        insp = inspect(orm)
        if relation_name in insp.unloaded:
            return []

        data = getattr(orm, relation_name)
        return [mapper(item) for item in (data or [])]
    except Exception:
        # Любая ошибка (например, доступ к незагруженному отношению) → пустой список
        return []
