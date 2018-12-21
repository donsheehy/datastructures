# Doubly-Linked Lists

Previously, we introduced the Deque ADT and we gave two implementations, one using a list and one using a linked list.
In our linked list implementation, all of the basic operations ran in constant time except `removelast`.
In this chapter, we're going to introduce a new data structure that allows us to do all the Deque operations in constant time.
The key idea will be to store two links in each node, one forwards and one backwards so that we can traverse the list in either direction.
In this **doubly-linked list**, removing from the end will be symmetric to removing from the beginning, with the roles of head and tail reversed.

When we create a new `ListNode`, we can specify the nodes before and after so that the appropriate links can be established.
We want it to always be true that `b == a.link` if and only if `a = b.prev` for any two nodes `a` and `b`.
To help ensure this invariant, we set `self.prev.link = self` and `self.link.prev = self` unless `prev` or `link` respectively are `None`.

```python {cmd id="_doublylinkedlist_00"}
class ListNode:
    def __init__(self, data, prev = None, link = None):
        self.data = data
        self.prev = prev
        self.link = link
        if prev is not None:
            self.prev.link = self
        if link is not None:
            self.link.prev = self
```

First, we'll look at adding items a `DoublyLinkedList`.
These operations are very similar to the `addfirst` operation on a `LinkedList`.
One has to do a little more work to update the `prev` node that was not present in our `LinkedList`.

```python {cmd continue="_doublylinkedlist_00" id="_doublylinkedlist_01"}
class DoublyLinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0

    def addfirst(self, item):
        if len(self) == 0:
            self._head = self._tail = ListNode(item, None, None)
        else:
            newnode = ListNode(item, None, self._head)
            self._head.prev = newnode
            self._head = newnode
        self._length += 1

    def addlast(self, item):
        if len(self) == 0:
            self._head = self._tail = ListNode(item, None, None)
        else:
            newnode = ListNode(item, self._tail, None)
            self._tail.link = newnode
            self._tail = newnode
        self._length += 1

    def __len__(self):
        return self._length
```

The code above is begging for refactoring.
It's clear that there is a lot of shared logic between the two methods.
We should use this as an opportunity to simplify the code.
In this case, we might consider the more general problem of adding a node between two other nodes.
We will just need to consider those cases where the nodes `before` or `after` or both are `None`.

```python {cmd continue="_doublylinkedlist_01", id="_doublylinkedlist_02"}
    def _addbetween(self, item, before, after):
        node = ListNode(item, before, after)
        if after is self._head:
            self._head = node
        if before is self._tail:
            self._tail = node
        self._length += 1

    def addfirst(self, item):
        self._addbetween(item, None, self._head)

    def addlast(self, item):
        self._addbetween(item, self._tail, None)
```

Symmetry is also apparent in the code to remove an item from either end.
As with the `add` methods, we factor out a (private) method that both use to remove a node and return its data.
It includes a little logic to detect if the head or tail or both change with the removal.

```python {cmd continue="_doublylinkedlist_02", id="_doublylinkedlist_03"}
    def _remove(self, node):
        before, after = node.prev, node.link
        if node is self._head:
            self._head = after
        else:
            before.link = after
        if node is self._tail:
            self._tail = before
        else:
            after.prev = before
        self._length -= 1
        return node.data

    def removefirst(self):
        return self._remove(self._head)

    def removelast(self):
        return self._remove(self._tail)
```

## Concatenating Doubly Linked Lists

There are several operations that are very fast on doubly linked lists compared to other lists.
One of the most useful is the ability to concatenate two lists.
Recall that the plus sign can be used to concatenate two `list` objects.

```python {cmd id="j44w4tnd"}
A = [1,2,3]
B = [4,5,6]
C = A + B
print(A)
print(B)
print(C)
```

For lists, concatenation creates a new list.
It takes time proportional to the length of the newly created list `C` and it doesn't modify the lists `A` or `B`.
For doubly linked lists, we could achieve the same asymptotic running time by incrementally building up a new list.
However, if we are allowed to modify the lists, the concatenation can be accomplished by pointing the tail of the first list at the head of the second.

```python {cmd continue="_doublylinkedlist_03", id="_doublylinkedlist_04"}

    def __iadd__(self, other):
        if other._head is None: return
        if self._head is None:
            self._head = other._head
        else:
            self._tail.link = other._head
            other._head.prev = self._tail
        self._tail = other._tail
        self._length = self._length + other._length

        # Clean up the other list.
        other.__init__()
        return self
```

```python {cmd continue="_doublylinkedlist_04"}
L = DoublyLinkedList()
[L.addlast(i) for i in range(11)]
B = DoublyLinkedList()
[B.addlast(i+11) for i in range(10)]

L += B

n = L._head
while n is not None:
    print(n.data, end = ' ')
    n = n.link
```

We have to be a bit careful about the differences between this concatenation operation and concatenation of regular lists.  With the doubly-linked list, concatenation empties the other list.  It does this so that we don’t have multiple doubly-linked lists with the same `ListNode`s.    That would be a problem if we tried to edit just one of the lists, because the changes would be reflected in the other list as well, possibly with disastrous consequences.
