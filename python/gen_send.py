def gen():
    x = yield
    z = yield f'**{x}**'
    try:
        y = yield
        yield 200
    except ValueError:
        yield 300

    yield z
    return

g = gen()

r1 = next(g)             # run up to line 2, waiting for input
r2 = g.send(100)         # x = 100 in line 2; run up to next yield (`yield '**100**'` in line 3)
r3 = g.send('hi')        # z = 'hi' in line 3; run up to line 5, waiting for input
r4 = g.throw(ValueError) # throw ValueError at line 5; run up to line 8
r5 = next(g)

print(r1)  # prints 'None'
print(r2)  # prints '**100**'
print(r3)  # prints 'None'
print(r4)  # prints '300'
print(r5)  # prints 'hi'
