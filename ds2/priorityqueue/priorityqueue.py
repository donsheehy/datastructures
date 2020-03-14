from ds2.priorityqueue import Entry, HeapPQ

class PriorityQueue(HeapPQ):
    def __init__(self,
                 items = (),
                 entries = (),
                 key = lambda x: x):
        self._key = key
        self._entries = [Entry(i, p) for i, p in entries]
        self._entries.extend([Entry(i, key(i)) for i in items])
        self._itemmap = {entry.item : index
                         for index, entry in enumerate(self._entries)}
        self._heapify()

    def insert(self, item, priority = None):
        if priority is None:
            priority = self._key(item)
        index = len(self._entries)
        self._entries.append(Entry(item, priority))
        self._itemmap[item] = index
        self._upheap(index)

    def _swap(self, a, b):
        L = self._entries
        va = L[a].item
        vb = L[b].item
        self._itemmap[va] = b
        self._itemmap[vb] = a
        L[a], L[b] = L[b], L[a]

    def changepriority(self, item, priority = None):
        if priority is None:
            priority = self._key(item)
        i = self._itemmap[item]
        self._entries[i].priority = priority
        # Assuming the tree is heap ordered, only one will have an effect.
        self._upheap(i)
        self._downheap(i)

    def removemin(self):
        L = self._entries
        item = L[0].item
        self._swap(0, len(L) - 1)
        del self._itemmap[item]
        L.pop()
        self._downheap(0)
        return item

    def __iter__(self):
        return self

    def __next__(self):
        if len(self) > 0:
            return self.removemin()
        else:
            raise StopIteration
