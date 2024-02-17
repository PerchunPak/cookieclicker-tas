"""Module for some useful utils."""
import asyncio
import typing as t
from functools import wraps

from loguru import logger

tooltip_lock = asyncio.Lock()
"""Lock for tooltip operations.

As in cookie clicker tooltip is a singleton, every time we want to get information
from it, we should not run into race conditions.
"""


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
_R = t.TypeVar("_R", bound=t.Any)  # type: ignore[misc] # Explicit "Any" is not allowed


def async_to_sync(f: t.Callable[_P, t.Awaitable[_R]]) -> t.Callable[_P, _R]:  # type: ignore[misc] # Explicit "Any" is not allowed
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))  # type: ignore[arg-type] # "Callable" != "Awaitable" for some reason

    return wrapper


def log(f: t.Callable[_P, t.Awaitable[_R]]) -> t.Callable[_P, t.Awaitable[_R]]:  # type: ignore[misc] # Explicit "Any" is not allowed
    @wraps(f)
    async def wrapper(*args, **kwargs):
        logger.trace(f"{f.__name__}({args=}, {kwargs=})")
        return await f(*args, **kwargs)

    return wrapper


def extract_number_from_string(s: str) -> float:
    return float(s.strip().removesuffix("s").removesuffix(" cookie").replace(",", ""))
