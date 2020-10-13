class It:
    def __iter__(self):
        print("It.__iter__ called")
        yield 4
        return 5


def gen2():
    yield 1
    yield 2
    return 3


def gen():
    x = yield
    z = yield f"**{x}**"
    try:
        y = yield
        yield 200
    except ValueError:
        yield 300

    yield z
    a = yield from gen2()
    yield a

    it = It()
    print("before yield from it")
    b = yield from it
    yield b
    return


g = gen()

r1 = next(g)  # run up to line 2, waiting for input
r2 = g.send(
    100
)  # x = 100 in line 2; run up to next yield (`yield '**100**'` in line 3)
r3 = g.send("hi")  # z = 'hi' in line 3; run up to line 5, waiting for input
r4 = g.throw(ValueError)  # throw ValueError at line 5; run up to line 8
r5 = next(g)
r6 = next(g)
r7 = next(g)
print("before get r8")
r8 = next(g)
print("before get r9")
r9 = next(g)
print("before get r10")
r10 = next(g)

print("-" * 30)

print(r1)  # prints 'None'
print(r2)  # prints '**100**'
print(r3)  # prints 'None'
print(r4)  # prints '300'
print(r5)  # prints 'hi'
print(r6)  # prints 1
print(r7)  # prints 2
print(r8)  # prints 3
print(r9)  # prints 4
print(r10)  # prints 5
