import asyncio


class It:
    def __iter__(self):
        print("It.__iter__")
        yield self  # !!! this __iter__ itself is a generator
        return None


def f():
    it = It()
    print("before yield from iterator obj")
    yield from it
    fut = asyncio.Future()

    print("before")
    res = yield from fut
    print("after")


g = f()

res = g.send(None)
print(f"{res = }")
print("---")
res = g.send(None)
print(f"{res = }")
