class It:
    def __iter__(self):
        print("It.__iter__")
        yield self  # !!! this __iter__ itself is a generator
        print("after yield self")
        yield 2
        return None


it = It()
print("before loop")
for x in it:
    print(x)
