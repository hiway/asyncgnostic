# asyncgnostic

Python functions agnostic towards being called with await or otherwise.


Example:

```
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
    print(await async_caller())
    print(sync_caller())


def sync_main():
    print(asyncio.run(async_caller()))
    print(sync_caller())



sync_main()
asyncio.run(async_main())
```