from ds2.queue import ListQueue as Queue

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

    def preorder(self):
        yield self.data
        for child in self.children:
            for data in child.preorder():
                yield data

    # Set __iter__ to be an alias for preorder.
    __iter__ = preorder

    def _postorder(self):
        node, childiter = self, iter(self.children)
        stack = [(node, childiter)]
        while stack:
            node, childiter = stack[-1]
            try:
                child = next(childiter)
                stack.append((child, iter(child.children)))
            except StopIteration:
                yield node
                stack.pop()                 

    def postorder(self):
        return (node.data for node in self._postorder())

    def _layerorder(self):
        node, childiter = self, iter(self.children)
        queue = Queue()
        queue.enqueue((node, childiter))
        while queue:
            node, childiter = queue.peek()
            try:
                child = next(childiter)
                queue.enqueue((child, iter(child.children)))
            except StopIteration:
                yield node
                queue.dequeue()                 

    def layerorder(self):
        return (node.data for node in self._layerorder())
