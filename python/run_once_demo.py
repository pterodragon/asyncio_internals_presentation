import asyncio

async def coro_stub():
    """
        From Python docs:
        sleep() always suspends the current task,
        allowing other tasks to run.
    """
    await asyncio.sleep(0)  # this is like "yield" in generator


async def coro_p():
    for _ in range(3):
        print('coro_p: 1')
        await coro_stub()
        print('coro_p:     2')
        await coro_stub()
        print('coro_p:         3')
        await coro_stub()

async def coro_q():
    for _ in range(3):
        print('coro_q:             a')
        await coro_stub()
        print('coro_q:                 b')
        await coro_stub()

async def coro_main():
    task_p = asyncio.create_task(coro_p())
    # await asyncio.sleep(0)
    print('before scheduling 2 tasks')
    task_q = asyncio.create_task(coro_q())
    await asyncio.wait([task_p, task_q])

asyncio.run(coro_main())
