# Binary Search Trees

Let's start with an ADT.  A **SortedMapping** is a mapping data type for which the keys are comparable.
It should support all the same operations as any other mapping as well as some other operations similar to those in a `SortedList` such as predecessor search.

## The Sorted Mapping ADT
A **sorted mapping** stores a collection of key-value pairs (*with comparable keys*) supporting the following operations.

  - `get(k)` - Return the value associate to the key `k`.  An error (`KeyError`) is raised if the given key is not present.

  - `put(k, v)` - Add the key-value pair `(k,v)` to the mapping.

  - `floor(k)` - Return a tuple `(k,v)` corresponding to the key-value pair in the mapping with the largest key that is less than or equal to `k`.

  - `remove(k)` - Remove the key-value pair with key `k` from the sorted mapping.  An error (`KeyError`) is raised if the given key is not present.


## Binary Search Tree Properties and Definitions

A tree is called a **binary tree** if every node has at most two children.
We will continue to assume that we are working with ordered trees and so we call the children `left` and `right`.
We say that a binary tree is a **binary search tree** if for every node `x`, all the keys in the subtree `x.left` are less than the key at `x` and all the keys in the subtree `x.right` are greater than the key of `x`.  This ordering property, also known as **the BST property** is what makes a binary search tree different from any other kind of binary tree.

```python {cmd output="html" hide}
from drawtrees import draw
from bstmapping import BSTMapping

T = BSTMapping()
for i in [3,1,0,2,5,4,6]:
    T[i] = None
draw(T, 150)
```

The BST property is related to a new kind of tree traversal, that was not possible with other trees.
Previously we saw *preorder* and *postorder* traversal of trees.
These traversals visit all the nodes of the tree.
The preorder traversal visits the root of each subtree before to visiting any of its descendants.
The postorder traversal visits all the descendants before visiting the root.
The new traversal we introduce here is called **inorder traversal** and it visits all the nodes in the left child prior to visiting the root and then visits all the nodes in the right child after visiting the root.
This order results in a traversal of the nodes *in sorted order according to the ordering of the keys*.

## A Minimal implementation

We're going to implement a sorted mapping using a binary search tree.
As we have already written an abstract class for packaging up a lot of the magic methods we expect from a mapping, we will inherit from that class to get started.  

Also, unlike in the previous section, we're going to distinguish between a class for the tree (`BSTMapping`) and a class for the nodes (`BSTNode`).
We will maintain a convention that the operations on the `BSTNode` class will operate on and return other `BSTNode` objects when appropriate, whereas the `BSTMapping` class will abstract away the existence of the nodes for the user, only returning keys and values.

Here is just the minimum requirements to be a `Mapping`.
It's a top down implementation, so it delegates all the real work to the `BSTNode` class.

```python {cmd id="_bstmapping_00"}
from mapping import Mapping

class BSTMapping(Mapping):
    def __init__(self):
        self._root = None

    def get(self, key):
        if self._root:
            return self._root.get(key).value
        raise KeyError

    def put(self, key, value):
        if self._root:
            self.root = self._root.put(key, value)
        else:
            self._root = BSTNode(key, value)

    def __len__(self):
        return len(self._root) if self._root else 0

    def _entryiter(self):
        if self._root:
            yield from self._root

    def floor(self, key):
        if self._root:
            floornode = self._root.floor(key)
            return floornode.key, floornode.value
        else:
            return None, None

    def remove(self, key):
        if self._root:
            self._root = self._root.remove(key)
        else:
            raise KeyError

    def __delitem__(self, key):
        self.remove(key)

```

The code above gives us almost everything we need.  There are a couple of mysterious lines to pay attention to.  One is the line in the `put` method that updates the root.  We will use this convention extensively.  As methods may rearrange the tree structure, such methods return the node that ought to be the new root of the subtree.  The same pattern appears in the `remove` function.

One other construct we haven't seen before is the `yield from` operation in the iterator.  This takes an iterable and iterates over it, yielding each item.  So, `yield from self._root` is the same as `for item in iter(self._root): yield item`.  It implies that our `BSTNode` class will have to be iterable.

Let's see how these methods are implemented.  We start with the initializer and some handy other methods.

```python  {cmd id="_bstmapping_01" continue="_bstmapping_00"}
class BSTNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self._length = 1

    def __len__(self):
        return self._length
```

The `get` method uses binary search to find the desired key.

```python  {cmd id="_bstmapping_02" continue="_bstmapping_01"}
    def get(self, key):
        if key == self.key:
            return self
        elif key < self.key and self.left:
            return self.left.get(key)
        elif key > self.key and self.right:
            return self.right.get(key)
        else:
            raise KeyError
```

Notice that we are using `self.left` and `self.right` as booleans.
This works because `None` evaluates to `False` and `BSTNode`'s always evaluate to `True`.
We could have implemented `__bool__` to make this work, but it suffices to implement `__len__`.  Objects that have a `__len__` method are `True` if and only if the length is greater than `0`.  This is the default way to check if a container is empty.  So, for example, it's fine to write `while L: L.pop()` and it will never try to pop from an empty list.  In our case, it will allow us to write `if self.left` to check if there is a left child rather than writing `if self.left is not None`.

Next, we implement `put`.  It will work by first doing a binary search in the tree.  If it finds the key already in the tree, it overwrites the value (keys in a mapping are unique).  Otherwise, when it gets to the bottom of the tree, it adds a new node.  

```python  {cmd id="_bstmapping_03" continue="_bstmapping_02"}
    def put(self, key, value):
        if key == self.key:
            self.value = value
        elif key < self.key:
            if self.left:
                self.left.put(key, value)
            else:
                self.left = BSTNode(key, value)
        elif key > self.key:
            if self.right:
                self.right.put(key, value)
            else:
                self.right = BSTNode(key, value)
        self._updatelength()


    def _updatelength(self):
        len_left = len(self.left) if self.left else 0
        len_right = len(self.right) if self.right else 0
        self._length = 1 + len_left + len_right
```

The `put` method also keeps track of the length, i.e. the number of entries in each subtree.

### The `floor` function

The `floor` function is just a slightly fancier version of `get`.
It also does a binary search, but it has different behavior when the key is not found, depending on whether the last search was to the left or to the right.  Starting from any node, if we search to the right and the result is `None`, then we return the the node itself.
If we search to the left and the result is `None`, we also return `None`.

```python  {cmd id="_bstmapping_04" continue="_bstmapping_03"}
    def floor(self, key):
        if key == self.key:
            return self
        elif key < self.key:
            return self.left.floor(key) if self.left else None
        elif key > self.key:
            return (self.right.floor(key) or self) if self.right else self
```

To parse the expressions above, it's helpful to remember that boolean operations on objects can evaluate to objects.  In particular `False or myobject` evaluates to `myobject`.  Use the python interactive shell to try out some other examples and to see how `and` behaves.

### Iteration

As mentioned above, binary search trees support inorder traversal.  The result of an inorder traversal is that the nodes are yielded *in the order of their keys*.

Here is an inorder iterator for a binary search tree implemented using recursive generators.  This will be fine in most cases.

```python  {cmd id="_bstmapping_05" continue="_bstmapping_04"}
    def __iter__(self):
        if self.left:
            yield from self.left
        yield self
        if self.right:
            yield from self.right
```

## Removal

To implement removal in a binary search tree, we'll use a standard algorithmic problem solving approach.
We'll start by thinking about how to handle the easiest possible cases.
Then, we'll see how to turn every case into an easy case.

The start of a removal is to find the node to be removed using binary search in the tree.
Then, if the node is a leaf, we can remove it without any difficulty.
It's also easy to remove a node with only one child because we can remove the node and bring its child up without violating the BST property.

The harder case come when the node to be removed has both a left and a right child.
In that case, we find the node with the largest key in its left subtree (i.e. the rightmost node).
We swap that node with our node to be removed and call `remove` again on the left subtree.
The next time we reach that node, we know it will have at most one child, because the node we swapped it with had no right child (otherwise it wasn't the rightmost before the swap).

A note of caution.
Swapping two node in a BST will cause the BST property to be violated.
However, the only violation is the node to be removed will have a key greater than the node that we swapped it with.
So, the removal will restore the BST property.

Here is the code to do the swapping and a simple recursive method to find the rightmost node in a subtree.

```python {cmd id="_bstmapping_06" continue="_bstmapping_05"}
    def _swapwith(self, other):
        self.key, other.key = other.key, self.key
        self.value, other.value = other.value, self.value

    def maxnode(self):
        return self.right.maxnode() if self.right else self
```

Now, we are ready to implement `remove`.
As mentioned above, it does a recursive binary search to find the node.
When it finds the desired key, it swaps it into place and makes another recursive call.
This swapping step will happen only once and the total running time is linear in the height of the tree.

```python cmd id="_bstmapping_07" continue="_bstmapping_06"}
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
        else: raise KeyError
        self._updatelength()
        return self
```

```python {cmd id="removal_example1"}
from drawtrees import draw
from bstmapping import BSTMapping

T = BSTMapping()
for i in [3,2,1,6,4,5,9,8,10]:
    T[i] = None
```

```python {cmd continue="removal_example1" output="html"}
draw(T)
```

```python {cmd id="removal_example2" continue="removal_example1" output="html"}
T.remove(6)
```

```python {cmd continue="removal_example2" output="html"}
draw(T)
```

```python {cmd id="removal_example3" continue="removal_example2" output="html"}
T.remove(3)
```

```python {cmd continue="removal_example3" output="html"}
draw(T)
```
