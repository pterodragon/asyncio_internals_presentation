import asyncio
import time
from functools import partial


def count_down(fut, c):
    print("count", c)
    if c == 0:
        fut.set_result("result!")
        return

    time.sleep(1)
    loop = asyncio.get_event_loop()
    loop.call_soon(partial(count_down, fut, c - 1))


# internally, coroutine == generator, but it uses a flag to check if it's proper "async"
# this decorator set the flag so Python internal thinks this is proper "async"
@asyncio.coroutine
def gen1():
    fut = asyncio.Future()

    loop = asyncio.get_event_loop()
    loop.call_soon(partial(count_down, fut, 2))

    # this "fut" will yield itself until result is set, then it yields the result
    res = yield from fut

    # Once you understand "yield from fut", "asyncio.sleep" is easy to understand
    # yield from asyncio.sleep(1)
    return res


async def coro1():
    g = gen1()
    return await g


coro1_res = asyncio.run(coro1())
print("coro1_res", coro1_res)
