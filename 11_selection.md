# Selection

Consider the following problem.

> Given a list of numbers, find the median element.

Recall that the median element is the one that would be in the middle if we sorted the list.
So, the following could would be correct.

```python
def median(L):
    L.sort()
    return L[len(L) // 2]
```

The code does rearrange the list and we'd have to decide if that was okay for our given list.
If we use a fast sorting algorithm, we can expect this algorithm to run in $O(n\log n)$ time.

Can we do better?
How about a linear time algorithm?

Let's consider a related problem, first.
If our goal is to find the second largest item in a list, we could do this in linear time as follows.

```python
def secondsmallest(L):
    a, b = None, None
    for item in L:
        if a is None or item <= b:
            a, b = item, a
        elif b is None or item <= a:
            b = item
    return b
```

We just stored a variable for each of the two largest we've seen so far and update them as we look at new items.
You could probably make this work for the third largest or more, but it would start to get cumbersome and slow, especially if you wanted to extract the median.

Some other approach will be necessary to compute the median in linear time.
Let's try divide and conquer.
To make this work, we're going to take an approach that often appears when dealing with recursion:

> **To solve a problem with recursion, sometimes it's easier to solve a harder problem.**

So, rather than solving **the median problem** directly, we will solve **the selection problem** defined as follows.

> **The Selection Problem:** Given a list of numbers and a number $k$, find the $k$th smallest number in the list.

## The `quickselect` algorithm

We can use a divide and conquer approach derived from `quicksort` to do selection.
The idea is to partition the list and then recursive do the selection on one part or the other.
Unlike `quicksort`, we only have to do a recursive search on one half of the list (as in binary search).
(Note that the smallest element will be returned for $k=1$, *not* $k=0$, so there are several cases where we add one to the pivot index.)

```python
def quickselect(L, k):
    return _quickselect(L, k, 0, len(L))

def _quickselect(L, k, left, right):
    pivot = partition(L, left, right)
    if k <= pivot:
        return _quickselect(L, k, left, pivot)
    elif k == pivot + 1:
        return L[pivot]
    else:
        return _quickselect(L, k, pivot + 1, right)

def partition(L, left, right):
    pivot = randrange(left, right)
    L[pivot], L[right -1] = L[right -1], L[pivot]
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

Just as with `quicksort`, we use a randomized pivot so that we can expect to eliminate a constant fraction of the list with each new step.  Unlike `quicksort`, we will not make a recursive call on both sides.  As a result, we'll see that the average running time is only $O(n)$.  That means we can do selection faster than we can sort, which makes sense, but it is *not obvious* how to do it.
We'll make the analysis formal below.

## Analysis

The `quickselect` algorithm is a **randomized algorithm**.  
The worst-case running time is bad.  If we are trying to select the largest element and the pivots all land on the smallest elements, then the running time will be quadratic.  

Instead, we'll analyze the **expected running time**. The word **expected** comes from probability and refers to the *average* over all random choices the algorithm makes.

Given a list of $n$ numbers, the partition function will pick a random element to serve as the *pivot*.
We say a pivot is *good* if it lands in the range of indices from $n/4$ to $3n/4$.
So, choosing randomly, there is a 50% chance of picking a good pivot.

With each recursive call, we get a smaller list.  Let's say that $n_i$ is the size of the list on the $i$th recursive call, so $n = n_0 > n_1 > \cdots > n_k$, where $k$ is the (unknown) number of recursive calls.  There is a $1/2$ probability of a good pivot at any step, so the expected value of $n_i$ can be bounded as follows.

\[
E[n_i] \le (1/2)\left(\frac{3E[n_{i-1}]}{4}\right) + (1/2)(E[n_{i-1}]) = \left(\frac{7}{8}\right)E[n_{i-1}].
\]

This bound combines two bounds, each that holds at least half the time, first the good pivot case where $n_i \le 3n_{i-1}/4$ and second, the bad pivot case, where at least $n_i \le n_{i-1}$.
The actual expectation will be smaller, but this upper bound suffices.

Repeating this fact by plugging it into itself (recursively) for smaller values gives the next bound in terms of $n$.

\[
E[n_i] \le \left(\frac{7}{8}\right) n_{i-1}
\le \left(\frac{7}{8}\right)^2 n_{i-2}
\le \left(\frac{7}{8}\right)^3 n_{i-3}
\le \cdots \le
\left(\frac{7}{8}\right)^i n.
\]

Each recursive call takes linear time, so the total running time will be

\[
T(n) = \sum_{i = 0}^k O(n_i) = O(\sum_{i=0}^k n_i).
\]

So, we need to bound the sum of the $n_i$s, but we only need to bound the expected (average) sum.  The most important fact in all of probability is the **linearity of expectations**.  It says that the sum of two expected values is the expected value of the sum.  We use it here to finish our analysis.

\[
E[T(n)] = O\left(\sum_{i=0}^k E[n_i]\right) \le
O\left(\sum_{i=0}^k \left(\frac{7}{8}\right)^i n\right) = O(n).
\]

The last step follows by the well-known equation for geometric series.  You should have seen it in a math class by now, but don't hesitate to look it up if you forgot it.

## One last time without recursion

The `quickselect` algorithm is an example of linear recursion.  Each function call makes just one more function call.  It's also **tail recursive** because that single recursive call is the last operation prior to returning.  So, as we've seen several times before, it's possible to eliminate the recursion and replace it with a single loop.  The code is below, but you might want to try to write this yourself to see if you understand both the algorithm and the process of tail recursion elimination.

```python
def quickselect(L, k):
    left, right = 0, len(L)
    while left < right:
        pivot = partition(L, left, right)
        if k <= pivot:
            right = pivot
        elif k == pivot + 1:
            return L[pivot]
        else:
            left = pivot + 1
      return L[left]
```

As long as the difference between left and right shrinks by a constant factor every couple of pivots, we can be sure to *prune* enough of the search to get a linear time algorithm.

## Divide-and-Conquer Recap

There are three main classes of divide-and-conquer algorithms and analyses that we've seen for lists.  

The first,and perhaps simplest, were those like binary search, where each recursive step takes constant time and makes a single recursive call on a list that is a constant times smaller.  The total running time in those cases is proportional to the depth of the recursion, $O(\log n)$.

The second class of recursive, divide-and-conquer algorithms we saw were binary recursion associated with sorting.  In those, the running time is linear plus the time to make recursive calls on shorter lists whose total length is $O(n)$.  In those cases, as long as the depth of the recursion is $O(\log n)$, the total running time is $O(n \log n)$.

Now, we have a third class of divide-and-conquer algorithms, those like `quickselect`.  Here, like in the sorting algorithms, the running time is linear plus the cost of recursive calls.  However, like in binary search, there is only one recursive call.  In these cases, as long as the subproblems shrink by a constant factor at each step, the running time will be $O(n)$.

## A Note on Derandomization

An algorithm that does not use randomness is called **deterministic**.  So far, all the algorithms we have covered are deterministic so we didn't need to make the distinction.  In the case of the selection problem, it's possible to solve it in linear time in the worst-case, without randomness.

If you recall the `quickselect` algorithm depends on getting an approximate median in order to reduce the length of the list by a constant fraction.
So, if you had an algorithm for finding the median in linear time, you could use it to choose the pivots in `quickselect` in order to get a linear-time algorithm.

That should sound a little wrong.
We started this whole section with the idea that we can solve the median problem using an algorithm for selection.
Now, we want to solve the selection problem using an algorithm for median.
Will we be stuck with a chicken and egg situation?

The algorithm is sometimes called the *median of medians* algorithm.  You can find more info about it online.
