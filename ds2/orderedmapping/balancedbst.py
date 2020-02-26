from ds2.mapping import Mapping

class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self._length = 1

    def newnode(self, key, value):
        return BSTNode(key, value)

    def get(self, key):
        if key == self.key:
            return self
        elif key < self.key and self.left:
            return self.left.get(key)
        elif key > self.key and self.right:
            return self.right.get(key)
        else:
            raise KeyError

    def put(self, key, value):
        if key == self.key:
            self.value = value
        elif key < self.key:
            if self.left:
                self.left = self.left.put(key, value)
            else:
                self.left = self.newnode(key, value)
        elif key > self.key:
            if self.right:
                self.right = self.right.put(key, value)
            else:
                self.right = self.newnode(key, value)
        self.updatelength()
        return self

    def updatelength(self):
        len_left = len(self.left) if self.left else 0
        len_right = len(self.right) if self.right else 0
        self._length = 1 + len_left + len_right

    def floor(self, key):
        if key == self.key:
            return self
        elif key < self.key:
            return self.left.floor(key) if self.left else None
        elif key > self.key:
            return (self.right.floor(key) or self) if self.right else self

    def rotateright(self):
        newroot = self.left
        self.left = newroot.right
        newroot.right = self
        self.updatelength()
        newroot.updatelength()
        return newroot

    def rotateleft(self):
        newroot = self.right
        self.right = newroot.left
        newroot.left = self
        self.updatelength()
        newroot.updatelength()
        return newroot

    def maxnode(self):
        return self.right.maxnode() if self.right else self

    def _swapwith(self, other):
        """
        Swaps the key and value of a node.
        This operation has the potential to break the BST property.
        Use with caution!
        """
        self.key, other.key = other.key, self.key
        self.value, other.value = other.value, self.value

    def remove(self, key):
        if key == self.key:
            if self.left is None: return self.right
            if self.right is None: return self.left
            self._swapwith(self.left.maxnode())
            self.left = self.left.remove(key)
        elif key < self.key and self.left:
            self.left = self.left.remove(key)
        elif key > self.key and self.right:
            self.right = self.right.remove(key)
        else:
            raise KeyError
        self.updatelength()
        return self

    def __iter__(self):
        if self.left: yield from self.left
        yield Entry(self.key, self.value)
        if self.right: yield from self.right

    def preorder(self):
        yield self.key
        if self.left: yield from self.left.preorder()
        if self.right: yield from self.right.preorder()

    def __len__(self):
        return self._length

    def __str__(self):
        return str(self.key) + " : " + str(self.value)

class BSTMapping(Mapping):
    Node = BSTNode

    def __init__(self):
        self._root = None

    def get(self, key):
        if self._root is None: raise KeyError
        return self._root.get(key).value

    def put(self, key, value):
        if self._root:
            self._root = self._root.put(key, value)
        else:
            self._root = self.Node(key, value)

    def floor(self, key):
        if self._root:
            floornode = self._root.floor(key)
            if floornode is not None:
                return floornode.key, floornode.value
        return None, None

    def remove(self, key):
        if self._root is None: raise KeyError
        self._root = self._root.remove(key)

    def _entryiter(self):
        if self._root:
            yield from self._root

    def preorder(self):
        if self._root:
            yield from self._root.preorder()

    def __len__(self):
        return len(self._root) if self._root else 0

    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right

