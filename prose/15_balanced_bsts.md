# Balanced Binary Search Trees

In the previous chapter, we saw how to implement a Mapping using a BST.
However, in the analysis of the main operations, it was clear that the running time of all the basic operations depended on the height of the tree.

A BST with $n$ nodes can have height $n-1$.
It's easy to get such a tree, just insert the keys in sorted order.
On the other hand, there always exists a BST with height $O(\log n)$ for any set of $n$ keys.
This is achieved by inserting the median first, followed by the medians of each half and so on recursively.
So, we have a big gap between the best case and the worst case.
Our goal will be to get as close as possible to the best case while keeping the running times of all operations proportional to the height of the tree.

We will say that a BST with $n$ nodes is **balanced** if the height of the tree is at most some constant times $\log n$.
To balance our BSTs, we want to avoid rebuilding the whole tree.
Instead, we'd like to make a minimal change to the tree that will preserve the BST property.

The most basic such operation is called a **tree rotation**.
It comes in two forms, `rotateright` and `rotateleft`.
Rotating a node to the right will move it to be the right child of its left child and will update the children of these nodes appropriately.
Here it is in code.

```python
def rotateright(self):
    newroot = self.left
    self.left = newroot.right
    newroot.right = self
    return newroot
```

Notice that `rotateright` returns the new root (of the subtree).
This is a very useful convention when working with BSTs and rotations.
Every method that can change the structure of the tree will return the new root of the resulting subtree.
Thus, calling such methods will always be combined with an assignment.
For example, if we want to rotate the left child of a node `parent` to the right, we would write `parent.left = parent.left.rotateright()`.

## A `BSTMapping` implementation

Here is the code for the `BSTMapping` that implements rotations.
We make sure to also update the lengths after each rotation.
The main difference with our previous code is that now, all methods that can change the tree structure are combined with assignments.
It is assumed that only `put` and `remove` will rearrange the tree, and so `get` and `floor` will keep the tree structure as is.

```python {cmd}
from mapping import Mapping, Entry


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

    def __str__(self):
        return str(list(self.preorder()))
```

### Forward Compatibility of Factories

We are looking into the future a little with this code.
In particular, we want this class to be easily extendable.
To do this, we don't create new instances of the nodes directly.
In the `BSTMapping` class, we have the assignment `Node = BSTNode` and create new nodes by writing `self.Node(key, value)` rather than `BSTNode(key, value)`.
This way, when we extend this class (as we will several times), we can use a different value for `Node` in order to produce different types of nodes without having to rewrite all the methods from `BSTMapping`.
Similarly, we use a `newnode` method in the `BSTNode` class.
A method that generates new instances of a class is sometimes called a **factory**.

With regards to *forward compatibility*, it's a challenge to walk the fine line between, good design and premature optimization.
In our case, the use of a factory to generate nodes only came about after the need was clear from writing subclasses.
This should be a general warning to students when reading code in textbooks.
One often only sees how the code ended up, but not how it started.
It's helpful to ask, "Why is the code written this way or that way?", but the answer might be that it will make later code easier to write.


## Weight Balanced Trees

Now, we're ready to balance our trees.
One way to be sure the tree is balanced is to have the key at each node `x` be the median of all the keys in the subtree at `x`.
Then, the situation would be analogous to binary search in a sorted `list`.
Moving down the tree, every node would have have as many nodes in its subtree than its parent.
Thus, after $\log n$ steps, we reach a leaf and so the BST would be balanced.

Having medians in every node a nice ideal to have, but it is both too difficult to achieve and too strong an invariant for balancing BSTs.
Recall that in our analysis of `quicksort` and `quickselect`, we considered *good pivots* to be those that lay in the middle half of the list (i.e. those with rank between $n/4$ and $3n/4$).
If the key in each node is a good pivot among the keys in its subtree, then we can also guarantee an overall height of $\log_{4/3} n$.

We'll say a node `x` is **weight-balanced** if

`len(x) + 1 < 4 * (min(len(x.left),len(x.right)) +  1)`.

It's easy enough to check this condition with our `BSTMapping` implementation because it keeps track of the length at each node.
If some change causes a node to no longer be weight balanced, we will recover the weight balance by rotations.
In the easiest case, a single rotation suffices.
If one is rotation is not enough, then two rotations will be enough.
We'll have to see some examples and do some simple algebra to see why.

The `rebalance` method will check for the balance condition and do the appropriate rotations.
We'll call this method after every change to the tree, so we can assume that the unbalanced node `x` is only just barely imbalanced.
Without loss of generality, let's assume `x` has too few nodes in its left subtree.
Then, when we call `x.rotateleft()`, we have to check that both `x` becomes weight balanced and also that its new parent `y` (the former right child of `x`) is weight balanced.
Clearly, `len(x) == len(x.rotateleft())` as both contain the same nodes.
So, there is an imbalance at `y` after the rotation only if its right child is too light.
In that case, we rotate `y` right before rotating `x` left.
This will guarantee that all the nodes in the subtree are weight balanced.

This description is not enough to be convincing that the algorithm is correct, but it is enough to write code.
Let's look at the code first and see the rebalance method in action.
Then, we'll go back and do the algebra to prove it is correct.

```python
from bstmapping import BSTMapping, BSTNode


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
```

The `toolight` method is for checking if a subtree has enough nodes to be a child of a weight balanced node.
We use it both to check if the current node is weight balanced and also to check if one rotation or two will be required.

The `put` and `remove` methods call the corresponding methods from the superclass `BSTNode` and then rebalance before returning.
We tried to reuse as much as possible our existing implementation.

## Height-Balanced Trees (AVL Trees)

The motivation for balancing our BSTs was to keep the height small.
Rather than balancing by weight, we could also try to keep the heights of the left and right subtrees close.
In fact, we can require that these heights differ by at most one.
Similar to weight balanced trees, we'll see if the height balanced property is violated and if so, fix it with one or two rotations.

Such height balanced trees are often called AVL trees.
In our implementation, we'll maintain the height of each subtree and use these to check for balance.
Often, AVL trees only keep the balance at each node rather than the exact height, but computing heights is relatively painless.

```python
from bstmapping import BSTMapping, BSTNode

def height(node):
    return node.height if node else -1

def update(node):
    if node:
        node.updatelength()
        node.updateheight()

class AVLTreeNode(BSTNode):
    def __init__(self, key, value):
        BSTNode.__init__(self, key, value)
        self.updateheight()

    def newnode(self, key, value):
        return AVLTreeNode(key, value)

    def updateheight(self):
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
        newroot = BSTNode.put(self, key, value)
        update(newroot)
        return newroot.rebalance()

    def remove(self, key):
        newroot = BSTNode.remove(self, key)
        update(newroot)
        return newroot.rebalance() if newroot else None

class AVLTreeMapping(BSTMapping):
    Node = AVLTreeNode

```

## Splay Trees

Let's add in one more balanced BST for good measure.
In this case, we won't actually get a guarantee that the resulting tree is balanced, but we will get some other nice properties.

In a **splay tree**, every time we get or put an entry, its node will get rotated all the way to the root.
However, instead of rotating it directly, we consider two steps at a time.
The `splayup` method looks two levels down the tree for the desired key.
If its not exactly two levels down, it does nothing.
Otherwise, it rotates it up twice.
If the rotations are in the same direction, the bottom one is done first.
If the rotations are in opposite directions, it does the top one first.

At the very top level, we may do only a single rotation to get the node all the way to the root.
This is handled by the `splayup` method in the `SplayTreeMapping` class.

A major difference from our previous implementations is that now, we will modify the tree on calls to `get`.
As a result, we will have to rewrite `get` rather than inheriting it.
Previously, get would return the desired value.
However, we want to return the new root on every operation that might change the tree.
So, which should we return?
Clearly, we need that value to return, and we also need to not break the tree.
Thankfully, there is a simple solution.
The splaying operation conveniently rotates the found node all the way to the root.
So, the `SplayTreeNode.get` method will return the new root of the subtree, and the `SplayTreeMapping.get` returns the value at the root.

```python
from bstmapping import BSTMapping, BSTNode

class SplayTreeNode(BSTNode):
    def newnode(self, key, value):
        return SplayTreeNode(key, value)

    def splayup(self, key):
        newroot = self
        if key < self.key:
            if key < self.left.key:
                newroot = self.rotateright().rotateright()
            elif key > self.left.key:
                self.left = self.left.rotateleft()
                newroot = self.rotateright()
        elif key > self.key:
            if key > self.right.key:
                newroot = self.rotateleft().rotateleft()
            elif key < self.right.key:
                self.right = self.right.rotateright()
                newroot = self.rotateleft()
        return newroot

    def put(self, key, value):
        newroot = BSTNode.put(self, key, value)
        return newroot.splayup(key)

    def get(self, key):
        if key == self.key:
            return self
        elif key < self.key and self.left:
            self.left = self.left.get(key)
        elif key > self.key and self.right:
            self.right = self.right.get(key)
        else:
            raise KeyError
        return self.splayup(key)

class SplayTreeMapping(BSTMapping):
    Node = SplayTreeNode

    def splayup(self, key):
        if key < self._root.key:
            self._root = self._root.rotateright()
        if key > self._root.key:
            self._root = self._root.rotateleft()

    def get(self, key):
        if self._root is None: raise KeyError
        self._root = self._root.get(key)
        self.splayup(key)
        return self._root.value

    def put(self, key, value):
        BSTMapping.put(self, key, value)
        self.splayup(key)
```
