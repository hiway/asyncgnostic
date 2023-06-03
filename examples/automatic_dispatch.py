import asyncio
from asyncgnostic import awaitable


# Define a sync function
def handler() -> str:  # type: ignore
    return "Running Sync"


# Pair the sync function with an async function
@awaitable(handler)
async def handler() -> str:
    return "Running Async"


# Call the function from sync context
def sync_main():
    print("sync context", handler())


# Call the function from async context
async def async_main():
    print("async context:", await handler())


# Run the sync and async functions
sync_main()
asyncio.run(async_main())
