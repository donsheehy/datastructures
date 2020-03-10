from ds2.mapping import Entry

class ListMappingSimple:
    def __init__(self):
        self._entries = []

    def put(self, key, value):
        for e in self._entries:
            if e.key == key:
                e.value = value
                return
        self._entries.append(Entry(key, value))

    def get(self, key):
        for e in self._entries:
            if e.key == key:
                return e.value
        raise KeyError
