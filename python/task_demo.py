import asyncio


async def coro2():
    print("a")
    return "hi"


async def coro():
    task = asyncio.create_task(coro2())
    print("b")
    return await task


res = asyncio.run(coro())
print(f"{res = }")
