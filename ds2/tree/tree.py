class Tree:
    def __init__(self, L):
        iterator = iter(L)
        self.data = next(iterator)
        self.children = [Tree(c) for c in iterator]

    def _listwithlevels(self, level, trees):
        trees.append("  " * level + str(self.data))
        for child in self.children:
            child._listwithlevels(level + 1, trees)

    def __str__(self):
        trees = []
        self._listwithlevels(0, trees)
        return "\n".join(trees)

    def __eq__(self, other):
        return self.data == other.data and self.children == other.children

    def height(self):
        if len(self.children) == 0:
            return 0
        else:
            return 1 + max(child.height() for child in self.children)

    def __contains__(self, k):
        return self.data == k or any(k in ch for ch in self.children)

