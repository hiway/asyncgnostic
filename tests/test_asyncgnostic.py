from asyncgnostic import awaited, awaitable


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
