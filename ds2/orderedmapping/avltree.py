from ds2.orderedmapping import BalancedBST, BalancedBSTNode

def height(node):
    return node.height if node else -1

def update(node):
    if node:
        node._updatelength()
        node._updateheight()

class AVLTreeNode(BalancedBSTNode):
    def __init__(self, key, value):
        BalancedBSTNode.__init__(self, key, value)
        self._updateheight()

    def newnode(self, key, value):
        return AVLTreeNode(key, value)

    def _updateheight(self):
        self.height = 1 + max(height(self.left), height(self.right))

    def balance(self):
        return height(self.right) - height(self.left)

    def rebalance(self):
        bal = self.balance()
        if bal == -2:
            if self.left.balance() > 0:
                self.left = self.left.rotateleft()
            newroot = self.rotateright()
        elif bal == 2:
            if self.right.balance() < 0:
                self.right = self.right.rotateright()
            newroot = self.rotateleft()
        else:
            return self
        update(newroot.left)
        update(newroot.right)
        update(newroot)
        return newroot

    def put(self, key, value):
        newroot = BalancedBSTNode.put(self, key, value)
        update(newroot)
        return newroot.rebalance()

    def remove(self, key):
        newroot = BalancedBSTNode.remove(self, key)
        update(newroot)
        return newroot.rebalance() if newroot else None

class AVLTree(BalancedBST):
    Node = AVLTreeNode
