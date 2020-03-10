from ds2.mapping import Mapping, ListMapping

class HashMapping(Mapping):
    def __init__(self, size = 100):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0

    def _entryiter(self):
        return (e for bucket in self._buckets for e in bucket._entryiter())

    def get(self, key):
        bucket = self._bucket(key)
        return bucket[key]

    def put(self, key, value):
        bucket = self._bucket(key)
        if key not in bucket:
            self._length += 1
        bucket[key] = value

        # Check if we need more buckets.
        if self._length > self._size:
            self._double()

    def __len__(self):
        return self._length

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]

    def _double(self):
        # Save the old buckets
        oldbuckets = self._buckets
        # Reinitialize with more buckets.
        self.__init__(self._size * 2)
        for bucket in oldbuckets:
            for key, value in bucket.items():
                self[key] = value
