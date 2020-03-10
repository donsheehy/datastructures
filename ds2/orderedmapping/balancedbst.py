from ds2.orderedmapping import BSTMapping, BSTNode

class BalancedBSTNode(BSTNode):
    def newnode(self, key, value):
        return BalancedBSTNode(key, value)

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
        self._updatelength()
        return self

    def rotateright(self):
        newroot = self.left
        self.left = newroot.right
        newroot.right = self
        self._updatelength()
        newroot._updatelength()
        return newroot

    def rotateleft(self):
        newroot = self.right
        self.right = newroot.left
        newroot.left = self
        self._updatelength()
        newroot._updatelength()
        return newroot

class BalancedBST(BSTMapping):
    Node = BalancedBSTNode

    def put(self, key, value):
        if self._root:
            self._root = self._root.put(key, value)
        else:
            self._root = self.Node(key, value)
