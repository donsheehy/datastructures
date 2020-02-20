from ds2.liststack import ListStack

class BadStack(ListStack):    
    def push(self, item):
        self._L.insert(0, item)

    def pop(self):
        return self._L.pop(0)

    def peek(self):
        return self._L[0]


