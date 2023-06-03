import asyncio
from asyncgnostic import awaitable


def handler() -> str:  # type: ignore
    return "Running Sync"


@awaitable(handler)
async def handler() -> str:
    return "Running Async"


def sync_main():
    print("sync context", handler())


async def async_main():
    print("async context:", await handler())


sync_main()
asyncio.run(async_main())
