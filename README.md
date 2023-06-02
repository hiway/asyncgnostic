# asyncgnostic

Python functions agnostic towards being called with await or otherwise.

> This is most likely a *BAD IDEA* and will slow down your code, treat is as a curiosity.

Example:

```python
import asyncio
from asyncgnostic import is_async


async def async_handler():
    return "Running async"


def sync_handler():
    return "Running sync"


def agnostic_handler():
    if is_async(stack_depth=2):
        return async_handler()
    else:
        return sync_handler()


async def async_caller():
    return await agnostic_handler()


def sync_caller():
    return agnostic_handler()


async def async_main():
    print("Calling from async_main, async:", await async_caller())
    print("Calling from async_main, sync:", sync_caller())


def sync_main():
    print("Calling from sync_main, async:", asyncio.run(async_caller()))
    print("Calling from sync_main, sync:", sync_caller())


sync_main()
asyncio.run(async_main())
```

Output:

```console
Calling from sync_main, async: Running async
Calling from sync_main, sync: Running sync
Calling from async_main, async: Running async
Calling from async_main, sync: Running sync
```
