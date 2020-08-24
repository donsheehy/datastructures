from ds2.mapping import Entry

class ListMapping:
    def __init__(self):
        self._entries = []

    def put(self, key, value):
        e = self._entry(key)
        if e is not None:
            e.value = value
        else:
            self._entries.append(Entry(key, value))

    def get(self, key):
        e = self._entry(key)
        if e is not None:
            return e.value
        else:
            raise KeyError

    def remove(self, key):
        e = self._entry(key)
        if e is not None:
            self._entries.remove(e)

    def _entry(self, key):
        for e in self._entries:
            if e.key == key:
                return e
        return None

    def __str__(self):
        return "{" + ", ".join(str(e) for e in self._entries) + "}"

    def __len__(self):
        return len(self._entries)

    def __contains__(self, key):    
        if self._entry(key) is None:
            return False
        else:
            return True

    def __iter__(self):
      return (e.key for e in self._entries)

    def values(self):
        return (e.value for e in self._entries)

    def items(self):
        return ((e.key, e.value) for e in self._entries)

    __getitem__ = get
    __setitem__ = put
