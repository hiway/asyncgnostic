from asyncgnostic import awaited, awaitable
import pytest


# Awaitable decorator setup


def increment(x: int) -> int:  # type: ignore
    return x + 1


@awaitable(increment)
async def increment(x: int) -> int:
    return x + 1


# Tests


def test_awaited_sync():
    assert not awaited()


async def test_awaited_async():
    async def _test():
        assert awaited()

    await _test()


async def test_awaitable_async():
    assert await increment(1) == 2


def test_awaitable_sync():
    assert increment(1) == 2


def test_strict_mode_different_return_types():
    def sync_func(x: int) -> int:
        return x + 1

    with pytest.raises(TypeError) as exc_info:

        @awaitable(sync_func)
        async def async_func(x: int) -> str:
            return str(x + 1)

    assert "must have the same return type" in str(exc_info.value)


def test_strict_mode_different_signatures():
    def sync_func(x: int, y: int = 0) -> int:
        return x + y

    with pytest.raises(TypeError) as exc_info:

        @awaitable(sync_func)
        async def async_func(x: int) -> int:
            return x + 1

    assert "must have the same signature" in str(exc_info.value)


def test_strict_mode_success():
    def sync_func(x: int, y: int = 0) -> int:
        return x + y

    @awaitable(sync_func)
    async def async_func(x: int, y: int = 0) -> int:
        return x + y

    assert sync_func(1, 2) == async_func(1, 2) == 3
    assert sync_func(1) == async_func(1) == 1


def test_awaitable_class_method():
    class Calculator:
        def sync_add(self, x: int, y: int) -> int:
            return x + y

        @awaitable(sync_add)
        async def add(self, x: int, y: int) -> int:
            return x + y

    calc = Calculator()
    assert calc.add(1, 2) == 3  # sync context


async def test_awaitable_class_method_async():
    class Calculator:
        def sync_add(self, x: int, y: int) -> int:
            return x + y

        @awaitable(sync_add)
        async def add(self, x: int, y: int) -> int:
            return x + y

    calc = Calculator()
    assert await calc.add(1, 2) == 3  # async context


def test_awaitable_static_method():
    class Calculator:
        @staticmethod
        def sync_add(x: int, y: int) -> int:
            return x + y

        @staticmethod
        @awaitable(sync_add)
        async def add(x: int, y: int) -> int:
            return x + y

    calc = Calculator()
    assert calc.add(1, 2) == 3  # sync context
    assert Calculator.add(1, 2) == 3  # sync context via class


async def test_awaitable_static_method_async():
    class Calculator:
        @staticmethod
        def sync_add(x: int, y: int) -> int:
            return x + y

        @staticmethod
        @awaitable(sync_add)
        async def add(x: int, y: int) -> int:
            return x + y

    calc = Calculator()
    assert await calc.add(1, 2) == 3  # async context
    assert await Calculator.add(1, 2) == 3  # async context via class


def test_awaitable_class_method_strict_mode():
    class Calculator:
        def sync_add(self, x: int) -> int:
            return x + 1

        with pytest.raises(TypeError) as exc_info:

            @awaitable(sync_add)
            async def add(self, x: int, y: int) -> int:
                return x + y

        assert "must have the same signature" in str(exc_info.value)


def test_non_strict_mode_different_return_types():
    def sync_func(x: int) -> int:
        return x + 1

    @awaitable(sync_func, strict=False)
    async def async_func(x: int) -> str:
        return str(x + 1)

    assert async_func(1) == 2  # sync context uses sync_func
    assert isinstance(async_func(1), int)


async def test_non_strict_mode_different_return_types_async():
    def sync_func(x: int) -> int:
        return x + 1

    @awaitable(sync_func, strict=False)
    async def async_func(x: int) -> str:
        return str(x + 1)

    result = await async_func(1)
    assert result == "2"  # async context uses async_func
    assert isinstance(result, str)


def test_non_strict_mode_different_signatures():
    def sync_func(x: int, y: int = 0) -> int:
        return x + y

    @awaitable(sync_func, strict=False)
    async def async_func(x: int) -> int:
        return x + 1

    assert async_func(1) == 1  # sync context uses sync_func with default y
    assert async_func(1, 2) == 3  # sync context uses sync_func with provided y


def test_non_strict_mode_class_method():
    class Calculator:
        def sync_add(self, x: int, y: int = 0) -> int:
            return x + y

        @awaitable(sync_add, strict=False)
        async def add(self, x: int) -> str:
            return str(x + 1)

    calc = Calculator()
    assert calc.add(1) == 1  # sync context
    assert calc.add(1, 2) == 3  # sync context with extra arg


async def test_non_strict_mode_class_method_async():
    class Calculator:
        def sync_add(self, x: int, y: int = 0) -> int:
            return x + y

        @awaitable(sync_add, strict=False)
        async def add(self, x: int) -> str:
            return str(x + 1)

    calc = Calculator()
    result = await calc.add(1)
    assert result == "2"  # async context
    assert isinstance(result, str)


async def test_awaited_in_list_comprehension():
    async def check():
        return [awaited(depth=1) for _ in range(1)][0]

    assert await check()


def test_awaited_in_generator_expression():
    def check():
        return next(awaited(depth=1) for _ in range(1))

    assert not check()


def test_awaitable_invalid_decoration():
    # Test decorating a sync function
    with pytest.raises(TypeError) as exc_info:

        @awaitable(lambda x: x)
        def sync_func(x):
            return x

    assert "can only decorate async functions" in str(exc_info.value)


def test_awaitable_nested_calls():
    def sync_outer(x: int) -> int:
        return x + 1

    def sync_inner(x: int) -> int:
        return x * 2

    @awaitable(sync_outer)
    async def outer(x: int) -> int:
        return x + 1

    @awaitable(sync_inner)
    async def inner(x: int) -> int:
        return x * 2

    # Test nested calls in sync context
    assert inner(outer(1)) == 4  # Should use sync functions


async def test_awaitable_nested_calls_async():
    def sync_outer(x: int) -> int:
        return x + 1

    def sync_inner(x: int) -> int:
        return x * 2

    @awaitable(sync_outer)
    async def outer(x: int) -> int:
        return x + 1

    @awaitable(sync_inner)
    async def inner(x: int) -> int:
        return x * 2

    # Test nested calls in async context
    assert await inner(await outer(1)) == 4  # Should use async functions
