class It:
    def __iter__(self):
        self.x = 0
        return self

    def __next__(self):
        self.x += 1
        if self.x >= 5:
            raise StopIteration
        return self.x


def f():
    for d in It():
        yield d


def g():
    yield from It()


for d in f():
    print(d)

print("---")

for d in g():
    print(d)
