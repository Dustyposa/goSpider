import asyncio

import anyio


async def anyio_task(n):
    print(f"start: {n}")
    await anyio.sleep(n)
    print(f"end: {n}")


async def async_task(n):
    print(f"start: {n}")
    await asyncio.sleep(n)
    print(f"end: {n}")


async def anyio_main():
    try:
        async with anyio.create_task_group() as tg:
            await tg.spawn(anyio_task, 1)
            await tg.spawn(anyio_task, 2)
    finally:
        # e.g. release locks
        print('cleanup')


async def async_main():
    task1 = asyncio.create_task(async_task(1))
    task2 = asyncio.create_task(async_task(2))
    await asyncio.gather(task1, task2)
    # await asyncio.wait([task1, task2])
    print('cleanup')

from anyio import create_task_group, create_semaphore, sleep, run


async def use_resource(tasknum, semaphore):
    async with semaphore:
        print('Task number', tasknum, 'is now working with the shared resource')
        await sleep(1)


async def main():
    semaphore = create_semaphore(10)
    async with create_task_group() as tg:
        for num in range(10):
            await tg.spawn(use_resource, num, semaphore)
from anyio import create_task_group, create_lock, sleep, run


async def use_resource(tasknum, lock):
    # async with lock:
    print('Task number', tasknum, 'is now working with the shared resource')
    await sleep(1)


async def main():
    lock = create_lock()
    async with create_task_group() as tg:
        for num in range(4):
            await tg.spawn(use_resource, num, lock)

from anyio import create_task_group, create_event, run


async def notify(event):
    await event.set()


async def main():
    event = create_event()
    async with create_task_group() as tg:
        await tg.spawn(notify, event)
        await event.wait()
        print('Received notification!')

from anyio import create_task_group, create_condition, sleep, run


async def listen(tasknum, condition):
    async with condition:
        await condition.wait()
        print('Woke up task number', tasknum)


async def main():
    condition = create_condition()
    async with create_task_group() as tg:
        for tasknum in range(6):
            await tg.spawn(listen, tasknum, condition)

        await sleep(1)
        async with condition:
            await condition.notify(1)

        await sleep(1)
        async with condition:
            await condition.notify(2)

        await sleep(1)
        async with condition:
            await condition.notify_all()

if __name__ == '__main__':
    # run(main)
    run(main)

    # anyio.run(anyio_main)
    # asyncio.run(async_main())
