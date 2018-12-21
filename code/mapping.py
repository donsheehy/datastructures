class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return "%d: %s" % (self.key, self.value)


class Mapping:

    # Child class needs to implement this!
    def get(self, key):
        raise NotImplemented

    # Child class needs to implement this!
    def put(self, key, value):
        raise NotImplemented

    # Child class needs to implement this!
    def __len__(self):
        raise NotImplemented

    # Child class needs to implement this!
    def _entryiter(self):
        raise NotImplemented        

    def __iter__(self):
      return (e.key for e in self._entryiter())

    def values(self):
        return (e.value for e in self._entryiter())

    def items(self):
        return ((e.key, e.value) for e in self._entryiter())

    def __contains__(self, key):
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __str__(self):
        return "{%s}" % (", ".join([str(e) for e in self._entryiter()]))

