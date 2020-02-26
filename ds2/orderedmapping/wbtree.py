from ds2.orderedmapping import BSTMapping, BSTNode

class WBTreeNode(BSTNode):
    def newnode(self, key, value):
        return WBTreeNode(key, value)

    def toolight(self, other):
        otherlength = len(other) if other else 0
        return len(self) + 1 >= 4 * (otherlength + 1)

    def rebalance(self):
        if self.toolight(self.left):
            if self.toolight(self.right.right):
                self.right = self.right.rotateright()
            newroot = self.rotateleft()
        elif self.toolight(self.right):
            if self.toolight(self.left.left):
                self.left = self.left.rotateleft()
            newroot = self.rotateright()
        else:
            return self
        return newroot

    def put(self, key, value):
        newroot = BSTNode.put(self, key, value)
        return newroot.rebalance()

    def remove(self, key):
        newroot = BSTNode.remove(self, key)
        return newroot.rebalance() if newroot else None

class WBTreeMapping(BSTMapping):
    Node = WBTreeNode

