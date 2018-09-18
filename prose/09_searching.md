# Binary Search

Binary search is a classic algorithm.
It is particularly nice to think about as a recursive algorithm.
If you are looking for an item in a sorted list, you break the list in half and repeat the search on whichever side could contain the missing element, which can be found by comparing with the median element.
Then, repeating on the smaller list is just a single recursive call.

```python
def bs(L, item):
    if len(L) == 0: return False
    median = len(L) // 2
    if item == L[median]:
        return True
    elif item < L[median]:
        return bs(L[:median], item)
    else:
        return bs(L[median + 1:], item)
```

This code, although correct, is not nearly as efficient as it could be.
To analyze it, we use the same technique as we will use for all recursive algorithms in this course.
We will count up *all* the operations that will be performed by the function except the recursive calls.
Then we will draw the tree of all recursive calls and add up the cost of each call.

In this case, the worst-case running time of `bs` on a list of length $n$ is $n/2$ plus a constant.
So, the first call costs $n/2$.
The second costs $n/4$.
The third costs $n/8$.
Adding them up gives a number close to $n$.
So, we are taking linear time to test membership.
We would be faster to just iterate one time through the list by using the `in` function (i.e. `list.__contains__`).

If we're going to do faster, we have to avoid all that slicing.
Let's only pretend to slice the list and instead pass the indices defining the range of the list we want to search.
Here is a first attempt.

```python
def bs(L, item, left = 0, right = None):
    if right is None: right = len(L)
    if right - left == 0: return False
    if right - left == 1: return L[left] == item
    median = (right + left) // 2
    if item < L[median]:
        return bs(L, item, left, median)
    else:
        return bs(L, item, median, right)
```

Note that we had to do a little work with default parameters so that we can still call this function as `bs(mylist, myitem)`.
This involves a check to see if `right is None` and sets it to be the length of the list if necessary.

When we analyze this recursive algorithm just as before, we see that all the operations take constant time, so the total running time will be proportional to the total number of recursive calls.
The tree of function calls is a single chain of length at most $O(\log n)$.
*(Why $\log(n)$?  This is the number of times you can cut $n$ in half before it gets down to $1$.)*
So, we see that the asymptotic running time is $O(\log n)$.

In the analysis, we observed that the tree of function calls is a single chain.
This is called **linear recursion**.
Here, we have a special case in which the function directly returns the result of the recursive function call.
That is called **tail recursion**.

In general, tail recursion can always be replaced by a loop.
The idea is to simply update the parameter variables and loop rather than making a recursive call.
Here is the idea in action.

```python
def bs(L, item):
    left, right = 0, len(L)
    while right - left > 1:
        median = (right + left) // 2
        if item < L[median]:
            right = median
        else:
            left = median
    return right > left and L[left] == item
```

Note that this solution is simpler to write than our original, and is also probably slightly faster.
It does require a little more thought to see why it's correct and why it runs in $O(\log n)$ time.

## The Sorted List ADT

  - `add(item)` - adds `item` to the sorted list.
  - `remove(item)` - removes the first occurrence of `item` from the sorted list. Raise a `ValueError` if the `item` is not present.
  - `__getitem__(index)` - returns the item with the given `index` in the sorted list.   This is also known as **selection**.
  - `__contains__(item)` - returns true if there is an item of the sorted list equal to `item`.
  - `__iter__` - returns an iterator over the sorted list that yields the items in sorted order.
  - `__len__` - returns the length of the sorted list.

Here is a very simple implementation of the sorted list ADT.

```python
class SimpleSortedList:
    def __init__(self):
        self._L = []

    def add(self, item):
        self._L.append(item)
        self._L.sort()

    def remove(self, item):
        self._L.remove(item)

    def __getitem__(self, index):
        return self._L[index]

    def __contains__(self, item):
        return item in self._L

    def __len__(self):
        return len(self._L)

    def __iter__(self):
        return iter(self._L)
```

This is a classic example of the Wrapper pattern.
The `list` storing the items is kept private so we can enforce that it stays ordered.
It looks a bit like a cheat to implement `add` in this way, but we'll see later as we cover sorting algorithms that this might be an efficient approach after all.

The one algorithm in this mix that seems most relevant to improve is the `__contains__` method.
Even though, we are just calling out to python's built-in method for checking membership in a list, we have some hoping of improving the efficiency because we know that the list is sorted.

Let's replace it with binary search as we implemented it above.

```python
class BSSortedList(SimpleSortedList):
    def __contains__(self, item):
        left, right = 0, len(self._L)
        while right - left > 1:
            median = (right + left) // 2
            if item < self._L[median]:
                right = median
            else:
                left = median
        return right > left and self._L[left] == item
```

We might also try to use binary search to find the index at which we want to insert a new node in order to speed up `add`.
Unfortunately, after finding the index, we still need to spend linear time in the worst-case to insert an item into a list at a particular index.
