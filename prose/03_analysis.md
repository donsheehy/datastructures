# Running Time Analysis

Our major goal in programming is to write code that is *correct*, *efficient*, and *readable*.
When writing code to solve a problem, there are many ways to write correct code.
When the code is not correct, we debug it.
When the code is inefficient, we may not notice when running small tests because we only see the problem when inputs get larger.
It can be much harder to track down problems with efficiency.

We want to develop a vocabulary for describing the efficiency of our code.
Sentences like "This code is fast" or "This code is slow" tell us very little.
How fast or slow is it?
Moreover, the same code will take different amounts of time and memory depending on the input.
It will also run faster on a faster computer.
So, our goals are challenging:
> We want to give a nuanced description of the efficiency of a program that adapts to *different inputs* and to *different computers*.

We will achieve both goals with **asymptotic analysis**.
To develop this theory, we will start by measuring the time taken to run some programs.
By simple experiments, we can observe how the running times change as the inputs get larger.
For example, a program that takes a list as input may run slower if that list has a million items than if it only has ten items, but maybe not.
It will depend on the program.

Next, we will give an accounting scheme for counting up the **cost** of a program.
This will assign costs to different operations.
The cost of the whole program will be the sum of the costs of all the operations executed by the program.
Often, the cost will be a function of the input size, rather than a fixed number.

Finally, we will introduce some vocabulary for classifying functions.
This is the asymptotic part of asymptotic analysis.
The **big-O** notation gives a very convenient way of grouping this (running time) functions into classes that can easily be compared.
Thus, we'll be able to talk about and compare the efficiency of different algorithms or programs without having to do extensive experiments.

Thinking about and analyzing the efficiency of programs helps us develop good habits and intuitions that lead to good design decisions.
The goal of increasing efficiency in our data structures will be the primary motivation for introducing new structures and new ideas
as we proceed.
## Timing Programs

To start, let's observe some differences in running time for different functions that do the same thing.
We might say these functions have the same behavior or the same **semantics**.

Here is a function that takes a list as input; it returns `True` if there are any duplicates and `False` otherwise.

```python {cmd id="duplicates1"}
def duplicates1(L):
    n = len(L)
    for i in range(n):
        for j in range(n):
            if i != j and L[i] == L[j]:
                return True
    return False

assert(duplicates1([1,2,6,3,4,5,6,7,8]))
assert(not duplicates1([1,2,3,4]))
```

A basic question that we will ask again and again is the following?

> How fast is this code?

The simplest answer to this question comes from simply running the program and measuring how long it takes.
We could do this as follows.

```python {cmd continue="duplicates1" id="j543h66u"}
import time

for i in range(5):
    n = 1000
    start = time.time()
    duplicates1(list(range(n)))
    timetaken = time.time() - start
    print("Time taken for n = ", n, ": ", timetaken)
```

<!-- Mention the choice of test example. -->

Notice that we see some variation in the time required.
This is caused by many factors, but the main one is that the computer is performing many other tasks at the same time.
It is running an operating system and several other programs at the same time.
Also, if run on different computers, one could expect to see wildly different results based on the speed of the processor and other differences between the computers.
For now, let's run the code several times and take the average to smooth them out for a given computer.
We'll wrap this idea in a general function that takes another function as input, and a length.
It runs the given function on lists of the given length and averages the time take per run.

```python {cmd continue="duplicates1" id="timetrials"}
import time

def timetrials(func, n, trials = 10):
    totaltime = 0
    start = time.time()
    for i in range(trials):
        func(list(range(n)))
        totaltime += time.time() - start
    print("average =%10.7f for n = %d" % (totaltime/trials, n))
```

We can now look at the average running time as the length of the list gets longer.
It's not surprising to see that the average time goes up as the length $n$ increases.

```python {cmd continue="timetrials" id="j543zqs2"}
for n in [50, 100, 200, 400, 800, 1600, 3200]:
    timetrials(duplicates1, n)
```

Let's try to make our code faster.
Simple improvements can be made by eliminating situations where we are doing unnecessary or redundant work.
In the `duplicates1` function, we are comparing each pair of elements twice because both `i` and `j` range over all $n$ indices.
We can eliminate this using a standard trick of only letting `j` range up to `i`.
Here is what the code would look like.

```python {cmd continue="timetrials", id="duplicates2"}
def duplicates2(L):
    n = len(L)
    for i in range(1,n):
        for j in range(i):
            if L[i] == L[j]:
                return True
    return False
```

```python {cmd continue="duplicates2", id="j544j8r7"}
for n in [50, 100, 200, 400, 800, 1600, 3200]:
    timetrials(duplicates2, n)
```

There is a python shortcut the kind of loop used in `duplicates2`.
The `any` function takes an iterable collection of booleans and returns `True` if any of the booleans are true.
You can make an iterable collection in an expression in the same way one does for comprehensions.
This can be very handy.

```python {cmd continue="timetrials" id="duplicates3"}
def duplicates3(L):
    n = len(L)
    return any(L[i] == L[j] for i in range(1,n) for j in range(i))
```

```python {cmd continue="duplicates3", id="j544qfui"}
for n in [50, 100, 200, 400, 800, 1600, 3200]:
    timetrials(duplicates3, n)
```

This last optimization reduces the number of lines of code and may be desirable for code readability, but it doesn't improve the speed.

If we want to make a real improvement, we'll need a substantial new idea.
One possibility is to sort the list and look at adjacent elements in the list.
If there are duplicates, they will be adjacent after sorting.

```python {cmd continue="timetrials" id="duplicates4"}
def duplicates4(L):
    n = len(L)
    L.sort()
    for i in range(n-1):
        if L[i] == L[i+1]:
            return True
    return False
```

```python {cmd continue="duplicates3", id="duplicates5"}
def duplicates5(L):
    n = len(L)
    L.sort()
    return any(L[i] == L[i+1] for i in range(n-1))

def duplicates6(L):
    s = set()
    for e in L:
        if e in s:
            return True
        s.add(e)
    return False

def duplicates7(L):
    return len(L) == len(set(L))

def duplicates8(L):
    s = set()
    return any(e in s or s.add(e) for e in L)
```

```python {cmd continue="duplicates5", id="j544qfur"}
for n in [50, 100, 200, 400, 800, 1600, 3200]:
    print("Quadratic: ", end="")
    timetrials(duplicates3, n)
    print("Sorting:   ", end="")
    timetrials(duplicates5, n)
    print("Sets:      ", end="")
    timetrials(duplicates7, n)
    print('---------------------------')
```


Some key ideas:
The Data Structures really matter.  The speed of the set membership testing or set construction gives a big improvement.
We made assumptions about the elements of the list, that they were comparable or hashable.  These assumptions can be thought of as assumptions about the *type* of the elements.  This is not the same as the class.  It's duck typing.  The assumption is that certain methods can be called.
The example also gives some practice using generator expressions.

The main important idea is that the running time depends on the size of the input.  The time goes up as the length goes up.
Sometimes, the gap between two pieces of code will increase as the input size grows.

## Example: Adding the first k numbers.

Below is a program that adds up the first $k$ positive integers and returns both the sum and time required to do the computation.

```python {cmd id="sumk1"}
import time

def sumk(k):
    start = time.time()

    total = 0
    for i in range(k+1):
        total = total + i
    end = time.time()

    return total, end-start
```

```python {cmd continue="sumk1" id="j54378j3"}
for i in range(5):
    print("Sum: %d, time taken: %f" % sumk(10000))
```

Notice that we see some variation in the time required.
This is caused by many factors, but the main one is that the computer is performing many other tasks at the same time.
It is running an operating system and several other programs at the same time.
Also, if run on different computers, one could expect to see wildly different results based on the speed of the processor and other differences between the computers.
For now, let's run the code several times and take the average to smooth them out for a given computer.

```python {cmd continue="sumk1" id="timetrials2"}
def timetrials(func, k, trials = 10):
    totaltime = 0
    for i in range(trials):
        totaltime += func(k)[1]
    print("average =%10.7f for k = %d" % (totaltime/trials, k))
```

```python {cmd continue="timetrials2" id="j5437vpd"}
timetrials(sumk, 10000)
timetrials(sumk, 100000)
timetrials(sumk, 1000000)
timetrials(sumk, 10000000)
```

Seeing the times for different values of `k` reveals a rather unsuprising pattern.
As `k` goes up by a factor of 10, the time required for `sumk` also goes up by a factor of `10`.
This makes sense, because it has to do about `k` additions and assignments.
To say it another way, the time is proportional to `k`.
We will often be more concerned with finding what the running time is proportional to than finding the exact time itself.
We expect to see this relationship between the running time and the input `k` regardless of what computer we run the code on.

The code we wrote seems to be correct, however, there is another, much simpler way to compute the sum of the numbers from `1` to `k` using a formula that is very important for this class.
It will show up again and again.
To prove that

\[
\sum_{i = 1}^k i = 1 + 2 + 3 + \cdots + k = k (k + 1) / 2,
\]

it suffices to observe that you can add the numbers in pairs, matching $i$ with $k-i + 1$ starting with $1$ and $k$.
There are $k/2$ such pairs and each adds up to $k+1$.
Let's use this formula to rewrite our `sumk` function and time it.

```python {cmd continue="timetrials2" id="j5439nl1"}
import time

def sumk2(k):
    start = time.time()
    total = (k*(k+1)//2)
    end = time.time()
    return total, end-start

timetrials(sumk2, 10000)
timetrials(sumk2, 100000)
timetrials(sumk2, 1000000)
timetrials(sumk2, 10000000)
timetrials(sumk2, 100000000)
```

This is much much faster.
Even as `k` becomes very large, it doesn't seem to slow down.


## Modeling the Running Time of a Program

We will introduce a general technique for describing and summarizing the number of operations required to run a piece of code, be it a single line, a function, or an entire program.
Along the way, we will develop a vocabulary for comparing the efficiency of algorithms that doesn't require us to run them and time them.

It's not enough to count lines of code.
A single line of code can do a lot of stuff.
Here's a one line function that does all kinds of stuff.
It creates a list of 200 items and sums all the entries for each of value of i from 0 to k-1 and returns a list of the results.

```python {cmd id="j543abkc"}
def f001(k):
    return [sum([i, i + 1] * 100) for i in range(k)]

print(f001(9))
```

Instead, we will want to count operations a little more carefully.
The unit we will use to describe the **running time** of an algorithm is the number of atomic operations.
This is not exactly a unit of time, but at some level, the atomic operations that we will describe can all be performed in a small number of clock cycles on your CPU and so correspond to a real amount of time.

*(Please don't say "runtime" as a replacement for "running time".  These are not the same thing!)*

Atomic operations include
 - arithmetic and boolean operations
 - variable assignment
 - accessing the value of a variable from its name
 - branching (jumping to another part of the code for if/for/while statements)
 - calling a function
 - returning from a function

Below, there is listings of the asymptotic running time of the most common operations on the standard python collections classes.
You should familiarize yourself with these listings.
In particular, you should be aware of which operations on collections produce a new copy of the collection.
For example, concatenation and slicing both produce a new collection and thus the running times are proportional to the length of the newly created collection.
In almost all cases, one can see the reason for the running times by understanding what work the algorithms must do and also how the data structure is laid out in memory.

### List Operations

| Operation Name          | Code      | Cost |
|-------------------------|-----------|:------:|
| index access            | `L[i]` | $1$ |
| index assignment        | `L[i] = newvalue` |	$1$ |
| Append                  | `L.append(newitem)`	| $1$ |
| Pop (from end of list)  | `L.pop()` | $1$ |
| Pop (from index `i`)    | `L.pop(i)`	| $n - i$ |
| Insert at index `i`     | `insert(i, newitem)` |	$n-i$ |
| Delete an item (at index `i`) | `del(item)` |	$n - i$ |
| Membership testing      | `item in L` | $n$ |
| Slice                   | `L[a:b]` | $b-a$
| Concatenate two lists   | `L1 + L2` | $n_1 + n_2$ |
| Sort                    | `L.sort()` | $n \log_2 n$

Note that these running times are the same for the other sequential collections, `list` and `str` assuming the operation exists for those immutable types.
For example, index access, membership testing, slicing, and concatenation all work.
Remember that slicing and concatenation produce new objects and don't change the originals.

### Dictionary Operations

Unlike the `list` operations, the costs of `dict` operations are a bit mysterious.
Some may seem downright impossible.
Should it really cost just one atomic operation to test if a given item is in a set of a billion elements?
There are three things to remember:
  1. We will study how dictionaries are implemented and how they exploit one of the wonderful, clever ideas of computer science.
  2. This is just a model, albeit a useful and accurate one.
  3. The actual cost is a kind of average.  It could take longer sometimes.

| Operation Name            | Code      | Cost |
|---------------------------|-----------|:------:|
| Get item                  | `D[key]` | $1$ |
| Set item                  | `D[key] = value` | $1$ |
| (key) membership testing  | `key in D` | $1$ |
| Delete an item by its key | `del D[key]` | $1$ |

### Set Operations

A `set` is very much like a `dict` where the entries have keys but no values.
They are implemented the same way and so, the running times for their common operations are the same.
Some set operations that correspond to our mathematical idea of a set do not correspond to operations on dictionaries.
Operations that produce a new set will leave the input sets unchanged.
Below, let $n_A$ be the size of set `A` and let $n_B$ be the size of set `B`.

| Operation Name            | Code      | Cost |
|---------------------------|-----------|:------:|
| Add a new item            | `A.add(newitem)` | $1$ |
| Delete an item            | `A.delete(item)` | $1$ |
| Union                     | <code>A &#124; B</code>   | $n_A + n_B$ |
| Intersection              | `A & B`   | $\min\{n_A, n_B\}$ |
| Set differences           | `A - B`   | $n_A$ |
| Symmetric Difference      | `A ^ B`   | $n_A + n_B$ |



## Asymptotic Analysis and the Order of Growth

The goal is not to predict exactly how much time an algorithm will take, but rather to predict the **order of growth** of the time as the input size grows.
That is, if we have algorithm that operates on a list of length $n$, the running time could be proportional to $n$.
In that case, the algorithm will take $100$ times longer on a list that is $100$ times longer.
A second algorithm might have a running time proportional to $n^2$ for inputs of length $n$.
Then, the algorithm will take $10000$ times longer on a list that is $100$ times longer.
Notice, that *the exact constant of proportionality is not important for these facts.*

The *size of the input* refers to the number of bits needed to encode it.
As we will be ignoring constant factors, we could just as easily refer to the number of words (a word is 64 bits) needed to encode it.
An integer or a float is generally stored in one word.
Technically, we can store some really big numbers in a python integer which would require many more words, but as a convention, we will assume that ints and floats fit in a constant number of bits.
This is necessary to assume that arithmetic takes constant time.

## Focus on the Worst Case

Usually, different inputs of the same length may have different running times.
The standard convention we will use most of the time is to consider the worst case.
We are looking for **upper bounds** on the running time.
If the algorithm has a running time that is better than the analysis predicts, that's okay.


## Big-O

We will almost always describe running times as a function of the input size.
That is, the running time on an input of size $n$ might be $5n^2 + 3n + 2$.
If we were to write this as a (mathematical) function of $n$, we could call it $f$ and write $f(n) = 5n^2 + 3n + 2$.
In this example, the $5n^2$ is by far the most important

The formal mathematical definition that allows us to ignore constant factors is called the **big-O notation**.
As a warmup example, we say that
\[
f(n) = O(n^2)
\]
if there exists a constant $c$ such that

\[
f(n) \le cn^2 \text{for all sufficiently large } n.
\]

This is correct for $f(n) = 5n^2 + 3n + 2$ because if we take $c = 6$, we see that as long as $n > 4$, we have

\[
f(n) = 5n^2 + 3n + 2 < 5n^2 + 4n < 5n^2 + n^2 \le 6n^2.
\]

The above inequalities came from repeated using the fact that $n > 4$.

We can now state the formal definition of the big-O notation:
Given (nondecreasing) functions $f$ and $g$, we say $f(n) = O(g(n))$ if there exist constants $c$ and $n_0$ such that for all $n>n_0$ we have $f(n) \le cg(n)$.

## The most important features of big-O usage

  1. The big-O *hides constant factors*.  Any term that does not depend on the size of the input is considered a constant and will be suppressed in the big-O.

  2. The big-O tells us about what will eventually be true *when the input is sufficiently large*.

These two features are present in the formal definition.
The constant $c$ is the constant that stands in for all other constant factors.
This constant also allows us to suppress lower order terms.
The constant $n_0$ is the threshold after which the inequality is true.


# Practical Use of the Big-O and Common Functions
Even though the definition of the big-O notation allows us to compare all kinds of functions, we will usually use it to simplify functions, eliminating extraneous constants and low order terms.
So, for example, you should write $O(n)$ instead of $O(3n)$ and $O(n^2)$ instead of $O(5n^2 + 3n + 2)$.
There are several functions that will come up so often that we will want to have them in our vocabulary.

 - **Constant Functions**, $O(1)$
 - **Logarithmic Functions**, $O(\log n)$
 - **Linear Functions**, $O(n)$
 - **"n Log n"**, $O(n\log n)$
 - **Quadratic Functions**, $O(n^2)$
 - **Polynomial Functions**, $O(n^k)$ for some constant $k$.
 - **Exponential Functions**, $O(2^n)$ (this is different from $2^{O(n)}$)
 - **Factorial Functions**, $O(n!)$

## Bases for Logarithms
You may have noticed that we didn't give a base for the logarithm above.
The reason is that inside the big-O, logarithms of any constant base are the same.
That is, $\log_a(n) = O(\log_b(n))$, where $a$ and $b$ are any two constants.
Here's the proof.
Let $c = \frac{1}{\log_b(a)}$ and $n_0 = 0$.  

\[
\log_a(n) = \frac{\log_b(n)}{\log_b(a)} \le c \log_b(n) \text{ for all }n>n_0.
\]

# Practice examples
In each of the following examples, assume the input is a list of length $n$.

```python
def f002(L):    
    newlist = []  # 2 creating a new list and variable assignment
    for i in L:   # loops n times
        if i % 2 == 0:  # 1
            newlist.append(i) # 1 (append is constant time on lists)
    return newlist  # 1 return
```

Let's count up the cost of each line of code.
The costs are in the comments.
So, the total cost is something like $2n+3$ in the worst case (i.e. when all the items are even).
We would report this as $O(n)$ and we would call this a **linear-time** algorithm, or sometimes simply a linear algorithm.

```python
def f003(L):
    x = 0   # 1
    for i in L:   # loop n times
        for j in L:   # loop n times
            x += i*j  # 3 two arithmetic operations and assignment
    return x # 1
```

Again, let's count up the cost of each line of code.
The costs are in the comments.
The inner loop costs $3n$ and it runs $n$ times, so the total for the whole method is $3n^2 + 2$.
We would report this as $O(n^2)$ and call this a **quadratic-time** algorithm, or sometimes simply a quadratic algorithm.

Here's an example we've seen several times.

```python
def f004(L):
    x = 0 # 1
    for j in range(1,len(L))  # loops n-1 times
        for i in range(j) # loops j times
            x += L[i] * L[j] # 5 two list accesses, two arithmetic operations and assignment
    return x # 1
```

It's a little trickier to figure this one out because the number of times the inner loop runs changes with each iteration of the outer loop.
In this case, it's not hard to add up the cost of each of the outer loops one at a time.
The first costs $5$, the second costs $10$, and so on to that the $j$th costs $5j$.
The total costs (including initializing `x` and returning is
\[
2 + \sum_{i=1}^{n-1}5i = 2 + 5\sum_{i=1}^{n-1}i = 2 + \frac{5n(n-1)}{2} = O(n^2).
\]

We will see this kind of sum often so it's worth recognizing it (both in the code and as a mathematical expression).
