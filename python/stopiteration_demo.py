def gen():
    yield 1
    return "generator return value"


res = []
g = gen()
res.append(g.send(None))
try:
    res.append(g.send(None))
except StopIteration as e:
    print("e.value", e.value)
    print("res", res)
