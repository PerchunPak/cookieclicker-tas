"""Module for some useful utils."""
import asyncio
import typing as t
from functools import wraps
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
(BASE_DIR / "data").mkdir(exist_ok=True)


class Singleton(type):
    """Metaclass to do Singleton pattern."""

    _instances: dict[type, t.Any] = {}  # type: ignore[misc] # Explicit "Any" is not allowed

    def __call__(cls, *args, **kwargs) -> t.Any:  # type: ignore[misc] # Explicit "Any" is not allowed
        """Actual logic in this class.

        See https://stackoverflow.com/a/6798042.
        """
        if cls not in cls._instances:
            instance = super(Singleton, cls).__call__(*args, **kwargs)

            if hasattr(instance, "_setup"):
                instance = instance._setup()
            cls._instances[cls] = instance

        return cls._instances[cls]


_P = t.ParamSpec("_P")
_R = t.TypeVar("_R", bound=t.Any)


def async_to_sync(f: t.Callable[_P, t.Awaitable[_R]]) -> t.Callable[_P, _R]:
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper
