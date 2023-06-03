import asyncio
from asyncgnostic import awaited


# Define a sync function
def sync_handler() -> str:  # type: ignore
    return "Running Sync"


# Define an async function
async def async_handler() -> str:
    return "Running Async"


# Define a dispatcher
def handler() -> str:
    if awaited():
        # If called from async context, call async function
        return async_handler()
    else:
        # If called from sync context, call sync function
        return sync_handler()


# Call the function from sync context
def sync_main():
    print("sync context", handler())


# Call the function from async context
async def async_main():
    print("async context:", await handler())


# Run the sync and async functions
sync_main()
asyncio.run(async_main())
