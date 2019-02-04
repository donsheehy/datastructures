# Dynamic Programming

The term **dynamic programming** refers to an approach to writing algorithms in which a problem is solved using solutions to the same problem on smaller instances.
Recall that this was the same intuition behind recursive algorithms.
Indeed, there are many instances in which you might arrive at a dynamic programming algorithm by starting with a recursive algorithm that is inefficient because it repeatedly makes recursive calls to a function with the exact same parameters, wasting time.

We start with the problem of giving change using the fewest coins.  Imagine that you have a list of coin amounts [1, 5, 10, 25] and an amount of change that you want to produce.
A first attempt at such a solution might be to assign the change in a **greedy** way.
In that approach, you would simply try to add the largest coin you can until you are done.
Here is an implementation.  *(Notice the relationship to Euclid's GCD algorithm)*

## A Greedy Algorithm

```python {cmd id="j32act34"}
def greedyMC(coinvalueList, change):
    coinvalueList.sort()
    coinvalueList.reverse()
    numcoins = 0
    for c in coinvalueList:
        # Add in as many coins as possible of the next largest value.
        numcoins += change // c
        # Update the amount of change left to return.
        change = change % c
    return numcoins

print(greedyMC([1,5,10,25], 63))
print(greedyMC([1, 21, 25], 63))
print(greedyMC([1, 5, 21, 25], 63))
```

Clearly, this does not work.
The second example returns 15 and the third returns 7.
In both cases, the right answer should have been 3 as can be achieved by returning three 21 cent coins.
The problem is not a bug in the code, but an incorrect algorithm.
The greedy solution does not work here.
Let's try recursion instead.

## A Recursive Algorithm

```python {cmd id="j32ad4km"}
def recMC(coinValueList, change):
   minCoins = change
   if change in coinValueList:
     return 1
   else:
      for i in [c for c in coinValueList if c <= change]:
         numCoins = 1 + recMC(coinValueList,change-i)
         if numCoins < minCoins:
            minCoins = numCoins
   return minCoins

# print(recMC([1,5,10,25],63)) # Seriously don't even try to run this
print(recMC([1, 21, 25],63))
print(recMC([1, 5, 21, 25],63))
```

This works, but it's very slow.  A natural thing to try here is to **memoize** solutions from previous recursive calls.
This way, we don't repeat work by computing the number of coins for a specific amount of change more than one time.
Don't forget to pass along the dictionary of known results when making recursive calls.

## A Memoized Version

```python {cmd id="j32adxkx"}
def memoMC(coinValueList, change, knownResults):
    minCoins = change
    if change in coinValueList:
        knownResults[change] = 1
        return 1
    elif change in knownResults:
        return knownResults[change]
    else:
        for i in [c for c in coinValueList if c <= change]:
            numCoins = 1 + memoMC(coinValueList, change-i, knownResults)
            if numCoins < minCoins:
                minCoins = numCoins
                knownResults[change] = minCoins
    return minCoins

print(memoMC([1,5,10,25],63, {}))

knownresults = {}
print(memoMC([1, 5, 10, 21, 25], 63, knownresults))
print(knownresults)
```

This is much faster and now can work with much larger instances.
It was slightly awkward that we had to pass in an empty dictionary to get things started, but that's not a big deal.
Let's look at the dictionary `knownresults` that gets populated by the algorithm.
It contains all but a few of the values from 1 to 63.
Maybe instead of recursive calls, starting with the full amount of change and working our way down, we could build up the dictionary of values starting with the small values and working our way up.
This is the essence of dynamic programming.

It happens that a list makes sense here because we want to access the items by their integer indices starting from 1.
In each step, the next best answer can be found by trying each coin, subtracting its value from the current value, and checking the list to find how many coins are needed to make up the rest of the change if that coin is used.

## A Dynamic Programming Algorithm

Finally, we can repackage this into a dynamic programming algorithm.
The idea is to explicitly fill in the table of all values, using previously computed values to compute new values.

```python {cmd id="j32akg27"}
def dpMakeChange(coinValueList, change):
    # Create a list to store the answers to the subproblems
    minCoins = [None]*(change + 1)

    # For each value from 0 to change, compute the min number of coins needed.
    for cents in range(change+1):
        # Assume at first that all 1's are used.
        minCoins[cents] = cents
        # Check if any coin leads to a better solution to our current best.
        for c in coinValueList:
            if cents >= c:
                minCoins[cents] = min(minCoins[cents], minCoins[cents - c] + 1)

    # Return just the element in the table corresponding to the desired value.
    return minCoins[change]

print(dpMakeChange([1,5,10,21,25], 63))
print(dpMakeChange([1,5,10,21,25], 64))

```

A major difference between the dynamic programming approach and the memoized recursion approach is that the dynamic program builds the results *from the bottom up*, while the recursive version works top down, starting work on the largest problem first and working down to the smaller problems as needed.
*Do either of these approaches correspond to the way that you solve programming problems?*

## Another example

In order to see dynamic programming as a general approach to solving problems, we need to see another example.
As with recursion, the key is to look for smaller problems to solve.
This is really a theme throughout this course.
All problems must be broken into smaller problems.
If those smaller problems are instances of the same problem we started with then maybe recursion or dynamic programming are appropriate.

The next problem we'll solve with dynamic programming is called the longest common subsequence (LCS) problem.
A **subsequence** of a string `s` is string `t` such that the characters of `t` all appear in `s` in the same order.
For example `'abc'` is a subsequence of `'xxxxxaxxxbxxxcxxxx'`

The input to the LCS problem is a pair of strings, we'll call them `X` and `Y`.
The output is the longest string that is a subsequence of both `X` and `Y`.

One view of this problem is that we want to find the smallest set of characters to remove from `X` and `Y` so that the results will be equal.
However, we don't want to try all possible subsequences.
There are $2^n$ subsequences of a string of length $n$.
That's too many!
Our code would never finish for even $n = 100$.

Here is the trick that cracks open this problem.
If `X` and `Y` end in the same character, then that character is the last character in the longest common subsequence.
That is, if `X[-1] == Y[-1]` then the `LCS(X,Y)` is `LCS(X[:-1], Y[:-1]) + X[-1]`.
On the other hand, if `X[-1] != Y[-1]`, then at least one of `X[-1]` or `Y[-1]` is *not* in the LCS.
In that case, `LCS(X,Y)` is the longer of `LCS(X[:-1],Y)` and `LCS(X,Y[:-1])`.
We could turn this into a very tidy recursive algorithm.

```python
def reclcs(X,Y):
    if X == "" or Y == "":
        return ""
    if X[-1] == Y[-1]:
        return reclcs(X[:-1], Y[:-1]) + X[-1]
    else:
        return max([reclcs(X[:-1], Y), reclcs(X, Y[:-1])], key = len)
```

However, when we run this on moderately size inputs, it seems to run forever.
It's not hard to see that if we had two long strings that didn't match any characters, then the tree of recursive calls would be a complete binary tree of depth $n$.
That's $2^n$ recursive calls.
However, there aren't that many distinct recursive calls.
Each such call is of the form `reclcs(X[:i], Y[:j])`, i.e. it takes the first `i` characters of `X` and the first `j` characters of `Y` for some `i` and `j`.
This means that there should only be $O(n^2)$ *distinct* recursive calls.  As $n^2$ is much smaller than $2^n$, many recursive calls are being repeated.
That's wasted work that we can avoid.
We could add memoization as before, but really, what we want is dynamic programming.
We'll store solutions to subproblems in a dictionary `t` so that `t[(i,j)] == LCS(X[:i], Y[:j])`.
We initialize the table with `""` for subproblems with `i = 0` or `j = 0` (the base case).
Here is the code.

```python
def lcs(X, Y):
    t = {}
    for i in range(len(X)+1): t[(i,0)] = ""
    for j in range(len(Y)+1): t[(0,j)] = ""

    for i, x in enumerate(X):
        for j, y in enumerate(Y):
            if x == y:
                t[(i+1,j+1)] = t[(i, j)] + x
            else:
                t[(i+1,j+1)] = max([t[(i, j+1)], t[(i+1, j)]], key = len)
    return t[(len(X), len(Y))]
```

The initialization takes linear time and the main pair of loops iterate $O(n^2)$ times.
The inner loop takes time proportional to the LCS in the worst case, because we will concatenate strings of that length.
The total running time is $O(kn^2)$ where $k$ is the length of the output.

Can you think of a way to get the running time down to $O(n^2)$?
This would require a different way to store solutions to subproblems.
