"""
Borrows heavily from Curio's meta.py module:

https://github.com/dabeaz/curio/blob/master/curio/meta.py

Curio is licensed under the BSD 3-Clause License.

https://github.com/dabeaz/curio/blob/master/LICENSE
"""

from sys import _getframe
from functools import wraps as _wraps
import inspect as _inspect


def awaited(depth=2, _cache={}) -> bool:
    """
    Check if function was called from async context.

    Args:
        depth (int): Stack depth to check. Default is 2.

    Returns:
        bool: True if function was called from async context, False otherwise.
    """
    f_code = _getframe(depth).f_code
    if f_code in _cache:
        # Return cached value
        return _cache[f_code]

    if f_code.co_flags & (
        _inspect.CO_COROUTINE
        | _inspect.CO_ITERABLE_COROUTINE
        | _inspect.CO_ASYNC_GENERATOR
    ):
        # Context is async
        _cache[f_code] = True
        return True
    else:
        # Context is possibly sync, except if the function is called
        # from a list comprehension or a generator expression.
        # The name of the function will start with '<', such as <listcomp> or <genexpr>.
        if f_code.co_flags & _inspect.CO_NESTED and f_code.co_name[0] == "<":
            return awaited(depth + 2)
        else:
            _cache[f_code] = False
            return False


def awaitable(sync_func, strict=True):
    """
    Decorator to pair a sync function with an async function.

    Args:
        sync_func (function): Sync function to pair with an async function.

    Returns:
        function: Decorated function.

    Example:
        >>> from asyncgnostic import awaitable

        >>> def increment(x: int) -> int:
        ...     return x + 1

        >>> @awaitable(increment)
        ... async def increment(x: int) -> int:
        ...     return x + 1

        >>> increment(1)
        2

        >>> await increment(1)
        2
    """

    def decorate(async_func):
        # Ensure the decorated function is async
        if not _inspect.iscoroutinefunction(async_func):
            raise TypeError("@awaitable can only decorate async functions")

        # Ensure sync and async functions have the same return type
        if (
            strict
            and _inspect.signature(sync_func).return_annotation
            != _inspect.signature(async_func).return_annotation
        ):
            raise TypeError(
                f"{sync_func.__name__} and async {async_func.__name__} must have the same return type"
            )

        # Ensure sync and async functions have the same signature
        if strict and _inspect.signature(sync_func) != _inspect.signature(async_func):
            raise TypeError(
                f"{sync_func.__name__} and async {async_func.__name__} must have the same signature"
            )

        @_wraps(async_func)
        def wrapper(*args, **kwargs):
            if awaited():
                # If called from async context, call async function
                return async_func(*args, **kwargs)
            else:
                # If called from sync context, call sync function
                return sync_func(*args, **kwargs)

        # Set docstring
        wrapper.__doc__ = async_func.__doc__ or sync_func.__doc__

        return wrapper

    return decorate
