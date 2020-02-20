from ds2.liststack import ListStack

class AnotherStack(ListStack):
    def pop(self):
        try:
            return self._L.pop()
        except IndexError:
            raise RuntimeError("pop from empty stack")

s = AnotherStack()
s.push(5)
s.pop()
s.pop()

