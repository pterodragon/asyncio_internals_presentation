import asyncio

# changed timeout to be always 0 in `base_events.py`
# result: selector calls selects many times in rapid succession


async def coro():
    f = asyncio.Future()
    await f


asyncio.run(coro())

