import asyncio


async def coro2():
    return "hi"


async def coro():
    task = asyncio.create_task(coro2())
    return await task


res = asyncio.run(coro())
print("res", res)
