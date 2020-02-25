# (Disjoint) Sets

The last chapter on mappings explains how we might hope to get constant time operations for many set operations.
It also makes clear why one cannot create a set of sets in python (at least, not directly).
The elements of a set must be hashable because they are stored in a hash table.
If you have sets that will not change, you can use the immutable `frozenset` data structure to store the sets and achieve many of of the benefits of `set`, while also being hashable.

However, there is one common data structuring problem that requires us to store a collection of sets that can change.
It is called the **Disjoint Sets** problem.
In this problem, we have a collection of things and the things are grouped in to disjoint sets.
We'd like to be able to quickly *find* if two things are in the same group.
On the other hand, we are sometimes *told* that two things are in the same group, in which case, we may need change our idea of the grouping, combining two groups into one.

A data structure to store a collection of disjoint sets is often called a **Union-Find** data structure, because it supports operations called, you guessed it, `union` and `find`.

## The Disjoint Sets ADT

- **`union(a, b)`** Replace the sets containing `a` and `b` with a single set that is their union.

- **`find(a, b)`** Return `True` is `a` and `b` are in the same set.  Otherwise, return `False`.

## A Simple Implementation

A very straightforward approach is to store the sets and a mapping that identifies each item with the set that contains it.
Because the sets are disjoint, there is a unique set that contains each item, so a mapping is appropriate.
The sets are the values in the mapping (not the keys), so there is no need for the sets to be hashable.
Here is an implementation.

```python {cmd id="_disjointsets.disjointsets_00"}
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
```

Here's a different idea.
We could just label the items.
If two items have the same label, then they are in the same set.
Union just relabels the items in one of the sets.
In this way, the sets themselves are implicit.

```python {cmd id="_disjointsets.disjointsets_01"}
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
```

Maybe this implementation is worse in some ways. It has to iterate through all the labels rather than just the subset that are connected. It does have the advantage that it does away with all the set operations in union. Again, this may not be better.
We can try to make our union operation much faster by changing fewer labels. In the next one, we will do this. Instead of mapping items to labels, we map them to an item that we'll call its parent. If every node has a single parent and there are no loops, then we get a forest. It is a collection of trees.

```python {cmd  id="_disjointsets.disjointsets_02"}
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
```

Is this much better? In many cases, it probably is, but not necessarily. I can easily construct an example where this code will take a long time. For example, I could force the forest to be a path. Then, calling the `_root` method can take time proportional to the number of items. If we're going to improve our worst-case running time, then we'll improve on those examples. We'll have to keep the paths short if possible.

# Path Compression

If we want to avoid traversing long paths to many times, we can just go and make them shorter each time we traverse them.  A simple way to do this is just to replace parents with gradnparents as we go up the tree.  This only requires one more line of code.  The affect is that the depth of every node on the path we traverse gets cut in half (plus one).  This means that the longest path can only get traversed $O(log n)$ times before it is compressed down to a single edge.

```python {cmd  id="_disjointsets.disjointsets_03"}
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
```

Without too much more effort, we can _really_ compress paths to the root by making a second pass.
In the first pass, we just find the root.  In the second pass, we update all the parents to point to the root.
Here is the updated code.

```python {cmd  id="_disjointsets.disjointsets_04"}
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
```

If you are really trying to optimize this, you may squeeze a little improvement by removing the redundancy involved in calling `_root` twice for each item in the `union` method (once in `find` and again in the `if` statement).

# Merge by Height

Another way you might try to keep paths short is to be just a little more careful about who gets to be the new root when doing a `union` operation.  The taller tree should be the new root, Then, the height will not increase unless you are merging two trees of the same height.

```python {cmd  id="_disjointsets.disjointsets_05"}
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
```

# Merge By Weight

Instead of looking at the heights of the trees, one could look at the number of nodes in the trees.  If one tree has more nodes, _maybe_ it is also taller.  The advantage over merge by height is that this information is not affected by path compression.  Therefore we can (and will soon) combine these tricks.

```python {cmd  id="_disjointsets.disjointsets_06"}
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
```

# Combining Heuristics

As mentioned before, we can use both heuristics, combining merge by weight and path compression.  it turns out that this is very efficient, both in theory and in practice.  The running time of $n$ operations is (as close as you will ever be able to tell) proportional to $n$.

```python {cmd  id="_disjointsets.disjointsets_07"}
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
```
