# Sorting

## The Quadratic-Time Sorting Algorithms

Before we dive into particular sorting algorithms, let's first ask an easier question:

> **Given a list `L`, determine if `L` is sorted or not.**

After a little, thought, you will probably come up with some code that looks like the following.

```python {cmd id="_sorting.dumbsort_00"}
def issorted(L):
    for i in range(len(L)-1):
        if L[i]>L[i+1]:
            return False
    return True
```

```python {cmd continue="_sorting.dumbsort_00"}
A = [1,2,3,4,5]
print(A, "is sorted:", issorted(A))

B = [1,4,5,7,2]
print(B, "is sorted:", issorted(B))
```

This is much better than the following, more explicit code.

```python {cmd}
def issorted_slow(L):
    for i in range(len(L)-1):
        for j in range(i+1, len(L)):
            if L[j] < L[i]:
              return False
    return True
```

The latter code checks that every pair of elements is in the right order.
The former code is more clever in that it only checks adjacent elements.
If the list is not sorted, then there will be two adjacent elements that will be out of order.
This is true because ordering relations are **transitive**, that is, if `a < b` and `b < c`, then `a < c`.
It's important to realize that we are using this assumption, because later, we will define our own ways of ordering items, and we will need to make sure this is true so that sorting even makes sense (if `a < b < c < a`, then what is the correct sorted order?).

Let's use the `issorted` method to write a sorting algorithm.
Instead of returning False when we find two elements out of order, we'll just fix them and move on.  Let's call this (for reasons to become clear) `dumbersort`.

```python {cmd id="_sorting.dumbsort_01" continue="_sorting.dumbsort_00"}
def dumbersort(L):
    for i in range(len(L)-1):
        if L[i]>L[i+1]:
            L[i], L[i+1] = L[i+1], L[i]
```

The main problem with this code is that *it doesn't sort the list*.

```python {cmd continue="_sorting.dumbsort_01"}
L = [5,4,3,2,1]
dumbersort(L)
print(L)
```

We should probably do it twice *or more*.  We could even repeat the algorithm until it works.

```python {cmd id="_sorting.dumbsort_02" continue="_sorting.dumbsort_01"}
def dumbsort(L):
    while (not issorted(L)):
        dumbersort(L)
```

```python {cmd continue="_sorting.dumbsort_02"}
L = [5,4,3,2,1]
dumbsort(L)
print(L)
```

Will it ever get the list sorted?  

How many times will we `dumberSort` the list?

After some thinking, you will notice that if `n = len(L)`, then looping `n-1` times is enough.  There are several different ways to see that this is correct.  You may see that every element in the list moves at least one place closer to its final location with each iteration.  

Another way to see that this works is to check that after calling `dumberSort(L)` one time, the largest element will move all the way to the end of the list and stay there through all subsequent calls.  Calling `dumberSort(L)` a second time will cause the second largest element to _bubble_ up to the second to last to last place in the list.  We are uncovering what is called an **invariant**, something that is true every time we reach a certain point in the algorithm.  For this algorithm, the invariant is that after `i` calls to `dumberSort(L)`, the last `i` items are in their final (sorted) locations in the list.  The nice thing about this invariant is that if it holds for `i = n`, then the whole list is sorted, and we can conclude the algorithm is correct.

At this point, we would test the code and think about refactoring.  Remember the DRY (**D** on't **R** epeat **Y** ourself) principle.  Because we know how many times to loop, we could just use a `for` loop.  


```python {cmd id="_sorting.bubblesortsimple"}
def bubblesort(L):
    for iteration in range(len(L)-1):
        for i in range(len(L)-1):
            if L[i]>L[i+1]:
                L[i], L[i+1] = L[i+1], L[i]
```

```python {cmd continue="_sorting.bubblesortsimple"}
alist = [30, 100000,54,26,93,17,77,31,44,55,20]
bubblesort(alist)
print(alist)
```

At this point, we have a correct algorithm and it's quite easy to bound its running time.  It's $O(n^2)$, a quadratic time algorithm.

We lost something compared to `dumbsort`, namely, we no longer stop early if the list is already sorted.  Let's bring that back.  We'll use a flag to check if any swaps were made.  

```python {cmd id="_sorting.bubblesort"}
def bubblesort(L):
    keepgoing = True
    while keepgoing:
        keepgoing = False
        for i in range(len(L)-1):
            if L[i]>L[i+1]:
                L[i], L[i+1] = L[i+1], L[i]
                keepgoing = True
```

Now, that we know an invariant that leads to a correct sorting algorithm, maybe we could work backwards from the invariant to an algorithm.  Recall, the invariant was that after `i` iterations of a loop, the `i` largest elements are in their final positions.  We can write an algorithm that just makes sure to achieve this, by selecting the largest among the first n-i elements and moving that element into place.

```python {cmd id="_sorting.selectionsort"}
def selectionsort(L):
    n = len(L)
    for i in range(n-1):
        max_index=0        
        for index in range(n - i):
            if L[index] > L[max_index]:
                max_index = index
        L[n-i-1], L[max_index] = L[max_index], L[n-i-1]
```

There is another invariant that we have implicitly considered previously when working with sorted lists.  Recall there, we assumed that we had a sorted list and one new element was added that had to moved into the correct position.  We saw several different variations of this.  We can turn this invariant into yet another sorting algorithm.  To keep it as close to possible as the previous attempts, we will say that the invariant is that after `i` iterations, the last `i` elements in the list are in sorted order.  

Do you see the difference between this and our previous invariant?

There are many ways we could enforce this invariant.  We'll do it by "bubbling" element `n-i` into position in the `i`th step.  Note this is not the final position, but rather the position that satisfies the invariant.

```python {cmd id="_sorting.insertionsortsimple"}
def insertionsort(L):
    n = len(L)
    for i in range(n):
        for j in range(n-i-1, n-1):
            if L[j]>L[j+1]:
                L[j], L[j+1] = L[j+1], L[j]
```

As before, we can make this algorithm go faster if the list is already sorted (or almost already sorted).  We stop the inner loop as soon as the element is in the right place

```python {cmd id="_sorting.insertionsort"}
def insertionsort(L):
    n = len(L)
    for i in range(n):
        j = n - i - 1
        while j < n - 1 and L[j]>L[j+1]:
            L[j], L[j+1] = L[j+1], L[j]
            j+=1
```

There is an important point to remember in the code above.  If `j == n-1`, then evaluating `L[j] < L[j+1]` would cause an error.  However, this code does not cause an error, because the expression `j < n - 1 and L[j]>L[j+1]` evaluates the first part first.  As soon as `j < n-1` evaluates to False, it doesn't need to evaluate the other clause of the `and`.  It skips it.

You often see `insertionsort` written in a way that keeps the sorted part of the list in the front rather than the end of the list.  

Could you write such an insertion sort?  Try it.

## Sorting in Python

Python has two main functions to sort a list.  They are called `sort()` and `sorted()`.  The difference is that the former sorts the list and the latter returns a new list that is sorted.  Consider the following simple demonstration.

```python
X = [3,1,5]
Y = sorted(X)
print(X, Y)

X.sort()
print(X)
```

```
[3, 1, 5] [1, 3, 5]
[1, 3, 5]
```

When working with your own classes, you may want to sort elements.  To do so, you only need to be able to compare elements.

In the following example, the elements are sorted by decreasing values of `b`: Python uses `__lt__` as the default comparator for sorting, so `Foo.__lt__` is used to sort objects of type `Foo`.  Then the list is sorted again, but a different comparator is used: `geta` is supplied as the key function, and the object returned by `geta` determines which `__lt__` attribute is used to sort. `Foo.geta` returns `a`, an integer, so `int.__lt__` is used.  Notice that the parameter `key` is a function which returns an object and not the evaluation of that function (e.g. `Foo.geta`, not `Foo.geta()`).

```python {cmd}
from random import randrange

class Foo:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __lt__(self, other):
        return other.b < self.b

    def __str__(self):
        return "(%d, %d, %d)" % (self.a, self. b, self. c)

    def geta(self):
        return self.a

L = [Foo(randrange(100),randrange(100), randrange(100)) for i in range(6)]
L.sort()    # sorts with the default function Foo.__lt__ (i.e. by decreasing b)
for foo in L:
    print(foo)

print("--------")

for foo in sorted(L, key = Foo.geta): # sorts according to the object returned by geta (i.e. by increasing a)
    print(foo)
```

If the key function returns a tuple, it will sort by the first element and break ties with subsequent elements.  This kind of sorting is called lexicographic because it is how you would sort words in alphabetical order.

Here is an example of sorting strings by their length (longest to shortest) using the alphabetical order (ignoring case) to break ties.

```python {cmd}
strings = "here are Some sample strings to be sorted".split()

def mykey(x):
    return -len(x), x.upper()

print(sorted(strings, key=mykey))
```
