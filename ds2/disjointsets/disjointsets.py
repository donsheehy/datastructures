class DisjointSetsMapping:
    def __init__(self, L):
        self._map = {item : {item} for item in L}

    def find(self, a, b):
        return a in self._map[b]

    def union(self, a, b):
        if not self.find(a,b):
            union = self._map[a] | self._map[b]
            for item in union:
                self._map[item] = union

class DisjointSetsLabels:
    def __init__(self, L):
        self._label = {item : item for item in L}

    def find(self, a, b):
        return self._label[a] is self._label[b]

    def union(self, a, b):
        if not self.find(a,b):
            for key, value in self._label.items():
                if value is self._label[b]:
                    self._label[key] = self._label[a]

class DisjointSetsForest:
    def __init__(self, L):
        self._parent = {item : item for item in L}

    def _root(self, item):
        while item is not self._parent[item]:
            item = self._parent[item]
        return item

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            self._parent[self._root(b)] = self._root(a)

# Path Compression halving as we go.  
# Every node on the path to root is updated to point to its grandparent.
class DisjointSetsPathCompression:
    def __init__(self, L):
        self._parent = {item : item for item in L}

    def _root(self, item):
        while item is not self._parent[item]:
            parent = self._parent[item]
            item, self._parent[item] = parent, self._parent[parent]
        return item

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            self._parent[self._root(b)] = self._root(a)

# Path compression with two passes.
# Retraverse the path to the root, pointing every node all the way up to the new root.
class DisjointSetsTwoPassPC:
    def __init__(self, L):
        self._parent = {item : item for item in L}

    def _root(self, item):
        root = item
        while root is not self._parent[root]:
            root = self._parent[root]
        self._compress(item, root)
        return root

    def _compress(self, item, newroot):
        while item is not newroot:
            item, self._parent[item] = self._parent[item], newroot

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            self._parent[self._root(b)] = self._root(a)

# Merge by height
class DisjointSetsMergeByHeight:
    def __init__(self, L):
        self._parent = {item : item for item in L}
        self._height = {item : 0 for item in L}

    def _root(self, item):
        while item is not self._parent[item]:
            item = self._parent[item]
        return item

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            if self._height[a] < self._height[b]:
                a,b = b,a
            self._parent[self._root(b)] = self._root(a)
            self._height[a] = max(self._height[a], self._height[b] + 1)

# Merge by weight
class DisjointSetsMergeByWeight:
    def __init__(self, L):
        self._parent = {item : item for item in L}
        self._weight = {item : 1 for item in L}

    def _root(self, item):
        while item is not self._parent[item]:
            item = self._parent[item]
        return item

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            if self._weight[a] < self._weight[b]:
                a,b = b,a
            self._parent[self._root(b)] = self._root(a)
            self._weight[a] += self._weight[b]

# Merge by weight and path compression
class DisjointSets:
    def __init__(self, L):
        self._parent = {item : item for item in L}
        self._weight = {item : 1 for item in L}

    def _root(self, item):
        root = item
        while root is not self._parent[root]:
            root = self._parent[root]
        self._compress(item, root)
        return root

    def _compress(self, item, newroot):
        while item is not newroot:
            item, self._parent[item] = self._parent[item], newroot

    def find(self, a, b):
        return self._root(a) is self._root(b)

    def union(self, a, b):
        if not self.find(a,b):
            if self._weight[a] < self._weight[b]:
                a,b = b,a
            self._parent[self._root(b)] = self._root(a)
            self._weight[a] += self._weight[b]
