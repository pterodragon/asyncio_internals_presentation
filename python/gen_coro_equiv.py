import asyncio


def gen1():
    print("in gen1")
    return 100
    yield  # just to force this function to be a generator


async def coro1():
    print("in coro1")
    return 100


coro1_res = asyncio.run(coro1())
print("coro1_res", coro1_res)

gen1_res = asyncio.run(gen1())
print("gen1_res", gen1_res)
