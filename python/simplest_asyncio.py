import asyncio

async def coro():
    return 'hi'

res = asyncio.run(coro())
print('res', res)
