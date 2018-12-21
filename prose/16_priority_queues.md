# Priority Queues

We're going to discuss a versatile and  fundamental data structure called a **priority queue**.  It will resemble a queue except that items all have a priority and will come out ordered by their priority rather than their order of insertion.

By this point, we know enough about different data structures that we will be able to implement this data structure in several different ways.  Eventually, we will introduce a data structure called a **heap** that will give good performance in many respects, but it won't be

## The Priority Queue ADT

The **Priority Queue ADT** is a data type that stores a collection of items with priorities (not necessarily unique) that supports the following operations.

  - `insert(item, priority)` - Add `item` with the given `priority`.

  - `findmin()` - Return the item with the minimum priority.  If there are multiple items with the minimum priority, ties may be broken arbitrarily.

  - `removemin()` - Remove and return the item with the minimum priority.  Ties are broken arbitrarily.

## Using a list

As with every ADT presented in this book, there is a simple, though not necessarily efficient, implementation using a list. Let's start with a list and put all the entries in the list. To find the min, we can iterate through the list.

```python
class SimpleListPQ:
    def __init__(self):
        self._L = []

    def insert(self, item, priority):
        self._L.append((item, priority))

    def findmin(self):
        return min(self._L, key = lambda x : x[1])[0]

    def removemin(self):
        item, priority = min(self._L, key = lambda x : x[1])
        self._L.remove((item, priority))
        return item
```

Although this code will work, there are a couple design decisions that are not great. First, there is something we might call *magical indices*.
As the data are stored as tuples, we have to use an index to pull out the priority or the item as needed.  This is an undocumented convention.  Someone reading the code would have to read the insert code to understand the `findmin` code. Also, there is some duplication in the use of `min` with the same `key` lambda expression for both `removemin` and `findmin`. These shortcomings can be our motivation to go back and clean it up, i.e. **refactor** it.

We'll make a class that stores the entries, each will have an `item` and a `priority` as attributes. We'll make the entries comparable by implementing `__lt__` and thus the comparison of entries will always just compare their priorities.

```python {cmd id="entry"}
class Entry:
    def __init__(self, item, priority):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority
```

Now, we can rewrite the list version of the priority queue.  It's almost the same as before, except, that by using the `Entry` class, the code is more explicit about the types of objects, and hopefully, easier to read and understand.

```python
class UnsortedListPQ:
    def __init__(self):
        self._entries = []

    def insert(self, item, priority):
        self._entries.append(Entry(item, priority))

    def findmin(self):
        return min(self._entries).item

    def removemin(self):
        entry = min(self._entries)
        self._entries.remove(entry)
        return entry.item
```

Let's analyze the running time of the methods in this class.
The `insert` method will clearly only require constant time because it is a single list append.  Both `findmin` and `removemin` take $O(n)$ time for a priority queue with $n$ items, because the `min` function will iterate through the while list to find the smallest priority entry.

The `findmin` would be much faster if the list were sorted.  Then we could just return the first item in the list.  An even better approach would sort the list backwards.  Then `removemin` could also be constant time, using the constant-time `pop` function on a list.

```python
class SortedListPQ:
    def __init__(self):
        self._entries = []

    def insert(self, item, priority):
        self._entries.append(Entry(item, priority))
        self._entries.sort(reverse = True)

    def findmin(self):
        return self._entries[-1].item

    def removemin(self):
        return self._entries.pop().item
```

I used a nice feature of the python `sort` method, a named parameter called `reversed` which, as one might guess, reverses the sorting order.

The asymptotic running time of both `findmin` and `removemin` is reduced to constant-time.  The `insert` method no longer runs in constant time, because it sorts.  This means that the running time will depend on the time it takes to sort.  In this case, assuming no other methods rearrange the (private!) `_entries` attribute, there will be only one entry out of sorted order, the one we just appended.  In this case, a good implementation of insertion sort would run in linear time (it only has to insert one item before everything is sorted).  Although, for code brevity, we called out to python's `sort` method, (which could take $O(n \log n)$-time) this is really a linear-time operation).

What we have with our two list implementations of the priority queue ADT is **tradeoff** between two operations.  In one case, we have fast `insert` and slow `removemin` and in the other we have slow `insert` and fast `removemin`.  Our goal will be to get all of the operations pretty fast.  We may not achieve constant time for all, but logarithmic-time is achievable.

## Heaps

The data structure we'll use for an efficient priority queue is called a **heap**.  Heaps are almost always used to implement a priority queue so that as you look at other sources, you might not see a distinction between the two ideas.  As we are using it, the priority queue is the ADT, the heap is the data structure.  

Matters are complicated by two other vocabulary issues.  First, there are many different kinds of heaps.  We'll study just one example, the so-called binary heap.  Second, the usual word used for the *priority* in a heap is "key".  This can be confusing, because unlike *keys* in mapping data structures, there is no requirement that priorities be unique.  We will stick with the word "priority" despite the usual conventions in order to keep these ideas separate.

We can think of a binary heap as a binary tree that is arranged so that smaller priorities are above larger priorities.  The name is apt as any good heap of stuff should have the big things on the bottom and small things on the top.  For any tree with nodes that have priorities, we say that the **tree is heap-ordered** if for every node, the priority of its children are at least as large as the the priority of the node itself.  This naturally implies that the minimum priority is at the root.

## Storing a tree in a list

Previously, we stored trees as a **linked data structure**.  This means having a node class that stores references to other nodes, i.e. the children.  We'll use the heap as an opportunity to see a different way to represent a tree.  We'll put the heap entries in a list and let the list indices encode the parent-child relationships of the tree.

For a node at index `i`, its left child will be at index `2 * i + 1` and the right child will be at index `2 * i + 2`.  This means that the parent of the node at index `i` is at index `(i-1) // 2`.  This mapping of nodes to indices puts the root at index `0` and the rest of the nodes appear level by level from left-to-right, top-to-bottom.  Using this mapping, we say a **list is heap-ordered** if the corresponding binary tree is heap-ordered.  This is equivalent to saying that for all $i > 0$, the priority of the entry at index $i$ is greater than or equal to the priority at index $(i-1) // 2$.

We will maintain the invariant that after each operation, the list of entries is heap-ordered.  To insert a new node, we append it to the list and then repeated swap it with its parent until it is heap-ordered.  This updating step will be called `_upheap` and is similar to the inner loop of an insertion sort.  However, unlike insertion sort, it only does at most $O(\log n)$ swap operations (each one reduces the index by half).

Similarly, there is a `_downheap` operation that will repeatedly swap an entry with its child until it's heap-ordered.  This operation is useful in the next section for building a heap from scratch.

```python
class HeapPQ:
    def __init__(self):
        self._entries = []

    def insert(self, item, priority):
        self._entries.append(Entry(item, priority))
        self._upheap(len(self._entries) - 1)

    def _parent(self, i):
        return (i - 1) // 2

    def _children(self, i):
        left = 2 * i + 1
        right = 2 * i + 2
        return range(left, min(len(self._entries), right + 1))

    def _upheap(self, i):
        L = self._entries
        parent = self._parent(i)
        if i > 0 and L[i] < L[parent]:
            L[i], L[parent] = L[parent], L[i]
            self._upheap(parent)

    def findmin(self):
        return self._entries[0].item

    def removemin(self):
        L = self._entries
        item = L[0].item
        L[0] = L[-1]
        L.pop()
        self._downheap(0)
        return item

    def _downheap(self, i):
        L = self._entries
        children = self._children(i)
        if children:
            child = min(children, key = lambda x: L[x])
            if L[child] < L[i]:
                L[i], L[child] = L[child], L[i]
                self._downheap(child)
```

## Building a Heap from scratch

Just using the public interface, one could easily construct a `HeapPQ` from a list of item-priority pairs.  For example, the following code would work just fine.

```python
pq = HeapPQ()
pairs = [(10, 10), (2, 2), (30, 30), (4,4)]
for item, priority in pairs:
    pq.insert(item, priority)
```

The `insert` method takes $O(\log n)$ time, so the total running time for this approach is $O(n \log n)$ time.  *You should double check that you believe this claim despite the fact that for each insertion, there are fewer than $n$ entries.*

Perhaps surprisingly, we can construct the `HeapPQ` in linear time.  We call this **heapifying a list**.  We will exploit the `_downheap` method that we have already written.  The code is deceptively simple.

```python
def _heapify(self):
    n = len(self._entries)
    for i in range(n):
        self._downheap(n - i - 1)
```

Look at the difference between the `heapify` code above and the `_heapify_slower` code below.  The former works from the end and "downheaps" every entry and the latter starts at the beginning and "upheaps" every entry.  Both are correct, but one is faster.

```python
def _heapify_slower(self):
    n = len(self._entries)
    for i in range(n):
        self._upheap(i)
```

They may seem to be the same, but they are not.  To see why, we have to look a little closer at the running time of `_upheap` and `_downheap`.  Consider the tree perspective of the list.  For `_upheap`, the running time depends on the depth of the starting node.  For `_downheap`, the running time depends on the height of the subtree rooted at the starting node.  Looking at a complete binary tree, half of the nodes are leaves and so `_downheap` will take constant time and `_upheap` will take $O(\log n)$ time.  Thus, `_heapify_slower` will take at least $\frac{n}{2}\log_2 n = O(n \log n)$ time.  

On the other hand, to analyze `_heapify`, we have to add up the heights of all the nodes in a complete binary tree.  Formally, this will be $n\sum_{i=1}^{\log_2 n}i/2^i$.  There is a cute trick to bound this sum.  Simply observe that if from every node in the tree, we take a path that goes left on the first step and right for every step thereafter, no two paths will overlap.  This means that the the sum of the lengths of these paths (which is also to the sum of the heights) is at most the total number of edges, $n-1$.  Thus, `_heapify` runs in $O(n)$ time.

## Changing priorities

There is another "standard" operation on priority queues.  It's called `reducepriority`.  It does what it says, reducing the priority of an entry.  This is very simple to implement in our current code if the index of the entry to change is known.  It would suffice to change the priority of the entry and call `_upheap` on that index.  

However, the usual way to reduce the priority is to specify the item and its new priority.  This requires that we can find the index of an item.  We'll do this by storing a dictionary that maps items to indices.  We'll have to update this dictionary every time we rearrange the items.  To make sure this happens correctly, we will add a method for swapping entries and use this whenever we make a swap.  

The full code including the `_heapify` method is given below.  This full version of the priority queue will be very useful for some graph algorithms that we will see soon.

```python {cmd continue="entry"}
class PriorityQueue:
    def __init__(self, entries = None):
        entries = entries or []
        self._entries = [Entry(i, p) for i, p in entries]
        self._itemmap = {i: index for index, (i,p) in enumerate(entries)}
        self._heapify()

    def insert(self, item, priority):
        index = len(self._entries)
        self._entries.append(Entry(item, priority))
        self._itemmap[item] = index
        self._upheap(index)

    def _parent(self, i):
        return (i - 1) // 2

    def _children(self, i):
        left, right = 2 * i + 1, 2 * i + 2
        return range(left, min(len(self._entries), right + 1))

    def _swap(self, a, b):
        L = self._entries
        va = L[a].item
        vb = L[b].item
        self._itemmap[va] = b
        self._itemmap[vb] = a
        L[a], L[b] = L[b], L[a]

    def _upheap(self, i):
        L = self._entries
        parent = self._parent(i)
        if i > 0 and L[i] < L[parent]:
            self._swap(i,parent)
            self._upheap(parent)

    def reducepriority(self, item, priority):
        i = self._itemmap[item]
        entry = self._entries[i]
        entry.priority = min(entry.priority, priority)
        self._upheap(i)

    def findmin(self):
        return self._entries[0].item

    def removemin(self):
        L = self._entries
        item = L[0].item
        self._swap(0, len(L) - 1)
        del self._itemmap[item]
        L.pop()
        self._downheap(0)
        return item

    def _downheap(self, i):
        L = self._entries
        children = self._children(i)
        if children:
            child = min(children, key = lambda x: L[x])
            if L[child] < L[i]:
                self._swap(i, child)
                self._downheap(child)

    def __len__(self):
        return len(self._entries)

    def _heapify(self):
        n = len(self._entries)
        for i in reversed(range(n)):
            self._downheap(i)

``` 
