import asyncio


def f():
    fut = asyncio.Future()

    print("before")
    res = yield from fut
    print("after")


g = f()
next(g)
