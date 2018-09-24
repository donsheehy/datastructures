# Sorting with Divide and Conquer

Previously, we saw some simple quadratic algorithms for sorting.
We saw `bubbleSort`, `selectionSort`, and `insertionSort`.
We considered all these algorithms from the perspective of correctness.
We wanted to have ways to argue that the result was indeed a sorted list, and only afterwards applied some optimizations (such as stopping early).
We used the idea of an **invariant**.
Specifically, it was a **loop invariant**, something that is true on each iteration of the loop.
We started with the invariant that after `i` iterations, the last `i` elements are in sorted order.

Invariants help us to reason about our code the same way we do with recursive algorithms.
Once the code is written, we assume the algorithm works on small examples in the same way we assume a loop invariant holds from a previous iteration of the loop.

Now, our goal is to write a faster sorting algorithm.

**Divide and Conquer** is a paradigm for algorithm design.
It usually consists of 3 (plus one) parts.
The first part is to **divide** the problem into 2 or more pieces.
The second part is the **conquer** step, where one solves the problem on the pieces.
The third part is the **combine** step where one combines the solutions on the parts into a solution on the whole.

The description of these parts leads pretty directly to recursive algorithms, i.e. using recursion for the conquer part.
The other part that appears in many such algorithms is a **base case**, as one might expect in a recursive algorithm.
This is where you deal with inputs so small that they cannot be divided.

## Mergesort

The most direct application of the Divide and Conquer paradigm to the sorting problem is the **mergesort** algorithm.
In this algorithm, all the difficult work is in the merge step.

```python
def mergeSort(L):
    # Base Case!
    if len(L) < 2:
        return

    # Divide!
    mid = len(L) // 2
    A = L[:mid]
    B = L[mid=]

    # Conquer!
    mergeSort(A)
    mergeSort(B)

    # Combine!
    merge(A, B, L)

def merge(A, B, L):   
    i = 0 # index into A
    j = 0 # index into B
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            L[i+j] = A[i]
            i = i + 1
        else:
            L[i+j] = B[j]
            j = j + 1
      # Add any remaining elements once one list is empty
      L[i+j:] = A[i:] + B[j:]
```

That last line might look a little strange.
The right side of the assignment is concatenating the remaining elements from the two lists (of which one should be empty).
Then, this list is assigned into a slice.
In its wonderfulness, python allows you to assign into a slice the same way you would assign into an index.

We could also use some more logic in the loop to avoid this last step, though I have found students disagree as to which approach is simpler.

```python {cmd}
def merge(A, B, L):   
    i, j = 0, 0
    while i < len(A) or j < len(B):
        if j == len(B) or (i < len(A) and A[i] < B[j]):
            L[i+j] = A[i]
            i = i + 1
        else:
            L[i+j] = B[j]
            j = j + 1
```

<!-- The same can be done without indices if one is comfortable removing elements from the input lists.

```python
def merge(A, B, L):
    C = []
    while A or B:
        if not B or (A and A[-1] > B[-1]):
            C.append(A.pop())
        else:
            C.append(B.pop())
    L[:] = reversed(C)
``` -->

The complex `if` statement above relies heavily on something called **short-circuited** evaluation of boolean expressions.
If we have a boolean operation like `or`, and the first operand is `True`, then we don't have to evaluate the second operand to find out that the overall result will be `True`.
Using this fact, python will not even evaluate the second operand.
Similarly, if we have an `and` expression and the first operand is `False`, then the second operand is never evaluated.
The key to remember is that the order does matter here.
The expression `(i < len(A) and A[i] < B[j]) or j == len(B)` is logically equivalent, but if we use this  expression instead, it will raise an IndexError when `j == len(B)`.

Short-circuit evaluation is *not* part of python magic, it's a standard feature in most programming languages.

### An Analysis

The analysis of `mergesort` will proceed in the usual way for recursive algorithms.
We will count the basic operations in the methods, not counting recursive calls.
Then, we will draw the tree of recursive calls and write down the cost of each function call in the tree.
Because the input size will change from call to call, the cost will also change.
Then, we add them all up to get the total running time.

The `merge` function for two lists whole length add up to $n$ takes $O(n)$ time.
This is because we only need to do a comparison and some assignment for each item that gets added to the final list (of which there are $n$).

In the tree of recursive calls, the top (or root) costs $O(n)$.
The next level has two calls on lists of length $n/2$.
The second level down has four calls of lists of length $n/4$.
On down the tree, each level $i$ has $2^i$ calls, each on lists of length $n/2^i$.
A nice trick to add these costs up, is to observe that the costs of all nodes on any given level sum to $O(n)$.
There are about $\log_2 n$ levels. (How many times can you divide $n$ by $2$ until you get down to $1$?)

So, we have $\log n$ levels, each costing $O(n)$, and thus, the total cost is $O(n \log n)$.


### Merging Iterators

The merge operation is another example of using some structure on our data (that two lists are themselves sorted) to perform some operation quickly (find the minimum overall element in constant time).
However, after you've written enough python, you might start to feel like you are doing something wrong if you are messing around with a lot of indices.
When possible, it is much nicer to use iterators.
We'll use this problem as an example to motivate some deeper study into iterators.

Recall that an object is an **Iterable** in python if it has a method called `__iter__` that returns an iterator,
and an **Iterator** is a object that has an `__iter__` method and a `__next__` method.
These magic methods are called *from the outside* as `iter(my_iterable)` and `next(my_iterator)`.
They are most commonly used by the `for` keyword either in for loops or in **generator expressions** as in comprehensions.

```python {cmd}
class SimpleIterator:
    def __init__(self):
        self._count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._count < 10:
            self._count += 1
            return self._count
        else:
            raise StopIteration

iterator1 = SimpleIterator()
for x in iterator1:
    print(x)

iterator2 = SimpleIterator()
L = [2 * x for x in iterator2]
```

Iterators are a fundamental pattern in object-oriented programming and they appear in other programming languages with slightly different methods.
For example, some programming languages have iterators that support a `hasnext` method that can tell in advance whether there is another item to iterate over.
In a standard python iterator, you simply try to get the next item and it will raise `StopIteration` if there isn't one.
This is an example of python's *easier to ask forgiveness than permission (EAFP)* approach.
Checking in advance is like asking for permission.
However, such a method can be handy.
With it, one might also want a method called `peek` that will return the next item without advancing past it.

Here is how one might implement these methods in python.
The `BufferedIterator` class below is built from any iterator.
It stays one step of the iteration ahead of the user and stores the next item in a buffer.

```python
class BufferedIterator:
    def __init__(self, i):
        self._i = iter(i)
        self._hasnext = True
        self._buffer = None
        self._advance()

    def peek(self):
        return self._buffer

    def hasnext(self):
        return self._hasnext

    def _advance(self):
        try:
            self._buffer = next(self._i)
        except StopIteration:
            self._buffer = None
            self._hasnext = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.hasnext():
            output = self.peek()
            self._advance()
            return output
        else:
            raise StopIteration
```

We can use this `BufferedIterator` to implement another iterator that takes two iterators and merges them as in the `merge` operation of `mergesort`.

```python
def merge(A, B):
    a = BufferedIterator(A)
    b = BufferedIterator(B)
    while a.hasnext() or b.hasnext():
        if not a.hasnext() or (b.hasnext() and b.peek() < a.peek()):
            yield next(b)
        else:
            yield next(a)
```

This iterator looks very different from our previous one.
First of all, it's not a class, but appears to just be a method.
This is a slick python way of defining a simple iterator.
The "method" here has `yield` statements instead of `return` statements.
Python recognizes this and creates a **generator** object.
Calling `merge` will return an object of type `generator`.
A `generator` is an iterator.
The easiest way to think of it is as a method that pauses every time it reaches `yield` and resumes when asked for the next item.
The magic here is explained by understanding that this really is packaged into an iterator object that is returned.

We can use this new `merge` iterator to write a new version of `mergesort`.

```python
def mergesort(L):
    if len(L) > 1:
        m = len(L) // 2
        A, B = L[:m], L[m:]
        mergesort(A)
        mergesort(B)
        L[:] = merge(A, B)
```

## Quicksort

The `mergesort` code does a lot of slicing.
Recall that this creates a copy.
Eventually, we will try to get to a version that doesn't do this.
A sorting algorithm, that just rearranges the elements in a single list is called an **in-place** sorting algorithm.
Before we get there, let's see the easiest version of `quicksort`.  One way to think about the motivation for `quicksort` is that we want to do divide and conquer, but we want the combine step to be as easy as possible.  Recall that in `mergesort`, most of our cleverness was devoted to doing the combining.
In `quicksort`, the harder step is the dividing.

```python
def quickSorted(L):
    #base case
    if len(L) < 2:
        return L[:]

    # Divide!
    pivot = L[-1]
    LT = [e for e in L if e < pivot]
    ET = [e for e in L if e == pivot]
    GT = [e for e in L if e > pivot]

    # Conquer
    A = quickSorted(LT)
    B = quickSorted(GT)

    # Combine
    return A + ET + B
```

Let's do an in-place version.  For this, we want to avoid creating new lists and concatenating them at the end.

```python {cmd}
def quicksort(L, left = 0, right = None):
    if right is None:
        right = len(L)

    if right - left > 1:    
        # Divide!
        mid = partition(L, left, right)

        # Conquer!
        quicksort(L, left, mid)
        quicksort(L, mid+1, right)

        # Combine!
        # Nothing to do!

def partition(L, left, right):
    pivot = right - 1
    i = left        # index in left half
    j = pivot - 1   # index in right half

    while i < j:
        # Move i to point to an element >= L[pivot]
        while L[i] < L[pivot]:
            i = i + 1

        # Move j to point to an element < L[pivot]
        while i < j and L[j] >= L[pivot]:
            j = j - 1

        # Swap elements i and j if i < j
        if i < j:
            L[i], L[j] = L[j], L[i]

    # Put the pivot in place.
    if L[pivot] <= L[i]:
        L[pivot], L[i] = L[i], L[pivot]
        pivot = i

    # Return the index of the pivot.
    return pivot

# Simple test to see if it works.
L = [5,2,3,1,4]
quicksort(L)
print(L)
```

Here is a version without all the comments.
It uses a helper function rather than using default parameters to handle the initial call.
It's helpful to look at at two different implementations of the same function and compare the different choices that were made between the two.

```python
def quicksort(L):
    _quicksort(L, 0, len(L))

def _quicksort(L, left, right):
    if right - left > 1:    
        mid = partition(L, left, right)
        _quicksort(L, left, mid)
        _quicksort(L, mid+1, right)

def partition(L, left, right):
    i, j, pivot = left, right - 2, right - 1
    while i < j:
        while L[i] < L[pivot]:
            i += 1
        while i < j and L[j] >= L[pivot]:
            j -= 1
        if i < j:
            L[i], L[j] = L[j], L[i]
    L[pivot], L[i] = L[i], L[pivot]    
    return i
```
