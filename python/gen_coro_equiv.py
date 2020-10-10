import asyncio


def gen2():
    print("in gen2")
    return 100
    # code never reaches here
    yield  # just force this to be a generator


def gen1():
    print("in gen1")
    res = yield from gen2()

    # Question: what does `yield` correspond to in a coroutine?
    # Hint: `yield` gives up control of the generator
    # yield
    return res


async def coro2():
    return 100


async def coro1():
    print("in coro1")
    res = await coro2()
    return res


coro1_res = asyncio.run(coro1())
print("coro1_res", coro1_res)

gen1_res = asyncio.run(gen1())
print("gen1_res", gen1_res)
