from ds2.mapping import Entry, ListMapping

class HashMapping:
    def __init__(self, size = 2):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0

    def put(self, key, value):
        m = self._bucket(key)
        if key not in m:
            self._length += 1
        m[key] = value

        # Check if we need more buckets.
        if self._length > self._size:
            self._double()

    def get(self, key):
        m = self._bucket(key)
        return m[key]

    def remove(self, key):
        m = self._bucket(key)
        m.remove(key)

    def __contains__(self, key):
        m = self._bucket(key)
        return key in m

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]

    def _double(self):
        # Save a reference to the old buckets.
        oldbuckets = self._buckets
        # Double the size.
        self._size *= 2
        # Create new buckets
        self._buckets = [ListMapping() for i in range(self._size)]
        # Add in all the old entries.
        for bucket in oldbuckets:
            for key, value in bucket.items():
                # Identify the new bucket.
                m = self._bucket(key)
                m[key] = value

    def __len__(self):
        return self._length

    def __iter__(self):
        for b in self._buckets:
            for k in b:
                yield k

    def values(self):
        for b in self._buckets:
            for v in b.values():
                yield v

    def items(self):
        for b in self._buckets:
            for k, v in b.items():
                yield k, v

    def __str__(self):
        # The following line is dangerous. It accesses a private attribute.
        # Thankfully, this will get factored out soon.
        itemlist = [str(e) for b in self._buckets for e in b._entries]
        return "{" + ", ".join(itemlist) + "}"

    __getitem__ = get
    __setitem__ = put
