    def _remove_at_index(self, index):
        L = self._entries
        self._swap(index, len(L) - 1)
        del self._itemmap[L[-1]]
        L.pop()
        self._downheap(index)

    def removemin(self):
        item = self._entries[0].item
        self._remove_at_index(0)
        return item

    def remove(self, item):
        self.remove_at_index(self._itemmap[item])

    def __next__(self):
        if len(self) > 0:
            return self.removemin()
        else:
            raise StopIteration
