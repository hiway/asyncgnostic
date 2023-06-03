# asyncgnostic

Python functions agnostic towards being called with await or otherwise.

Uses [multiple dispatch](https://en.wikipedia.org/wiki/Multiple_dispatch)
to automatically call asynchronous or synchronous function based on calling context.

## Example:

```python
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
```

Output:

```console
sync context Running Sync
async context: Running Async
```
## Credits:

Gratefully borrowed improvements from [curio](https://github.com/dabeaz/curio/).

Reference:
  - https://mastodon.sharma.io/@harshad/110476942596328864
  - https://mastodon.social/@dabeaz/110477080111974062
  - https://github.com/dabeaz/curio/blob/master/curio/meta.py
