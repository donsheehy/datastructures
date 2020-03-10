from ds2.mapping import ListMapping

class HashMappingSimple:
    def __init__(self):
        self._size = 100
        self._buckets = [ListMapping() for i in range(self._size)]

    def put(self, key, value):
        m = self._bucket(key)
        m[key] = value

    def get(self, key):
        m = self._bucket(key)
        return m[key]

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]
