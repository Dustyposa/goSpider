import asyncio
import time
from typing import List


async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)


async def synchronization_main():
    print(f"started at {time.strftime('%X')}")

    await say_after(1, 'hello')
    await say_after(2, 'world')

    print(f"finished at {time.strftime('%X')}")


async def wait_coroutine(coroutines):
    for i in coroutines:
        await i


async def asynchronization_main():
    print(f"started at {time.strftime('%X')}")
    coroutine_list = list()
    coroutine_list.append(asyncio.create_task(say_after(1, 'hello')))
    coroutine_list.append(asyncio.create_task(say_after(2, 'asyncio')))
    await wait_coroutine(coroutine_list)
    print(f"finished at {time.strftime('%X')}")


async def factorial(name, number):
    f = 1
    for i in range(2, number + 1):
        print(f"Task {name}: Compute factorial({i})...")
        await asyncio.sleep(1)
        f *= i
    print(f"Task {name}: factorial({number}) = {f}")


async def gather_main():
    # Schedule three calls *concurrently*:
    await asyncio.gather(
        factorial("A", 2),
        factorial("B", 3),
        factorial("C", 4),
    )


asyncio.run(gather_main())

