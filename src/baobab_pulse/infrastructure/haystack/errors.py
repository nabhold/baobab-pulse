"""Haystack/provider exception translation (item 120).

Nothing outside ``infrastructure.haystack`` ever sees a raw
``haystack.core.errors.*`` or provider-SDK exception. Every call into
Haystack from this package is wrapped so the rest of Pulse only ever
catches :class:`PulseHaystackError`.
"""

from __future__ import annotations

from collections.abc import Callable, Coroutine
from typing import Any, TypeVar

from baobab_pulse.domain.shared.errors import PulseError

T = TypeVar("T")


class PulseHaystackError(PulseError):
    """Raised in place of any exception a Haystack pipeline/component/tool
    call raised. The original exception is always chained (``raise ... from
    exc``) for local debugging, but callers outside this package should
    never need to inspect it."""


def translate_exceptions(operation: str) -> Callable[[Callable[..., T]], Callable[..., T]]:
    """Decorator: wrap a synchronous Haystack call, translating any
    exception into :class:`PulseHaystackError`."""

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return func(*args, **kwargs)
            except PulseError:
                raise
            except Exception as exc:  # noqa: BLE001 -- deliberate catch-all at the ACL boundary
                raise PulseHaystackError(f"{operation} failed: {exc}") from exc

        return wrapper

    return decorator


def translate_async_exceptions(
    operation: str,
) -> Callable[[Callable[..., Coroutine[Any, Any, T]]], Callable[..., Coroutine[Any, Any, T]]]:
    """As :func:`translate_exceptions`, for an ``async def`` Haystack call."""

    def decorator(func: Callable[..., Coroutine[Any, Any, T]]) -> Callable[..., Coroutine[Any, Any, T]]:
        async def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                return await func(*args, **kwargs)
            except PulseError:
                raise
            except Exception as exc:  # noqa: BLE001 -- deliberate catch-all at the ACL boundary
                raise PulseHaystackError(f"{operation} failed: {exc}") from exc

        return wrapper

    return decorator
