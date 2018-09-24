# Recursion

Recursion is an important idea across computer science.
For us, in learning data structures and basic algorithms, there are several ways to both think about and use recursion.
At its simplest, one can think of **recursion** as: *when a function calls itself*.

Although true, this definition doesn't really tell us how or why to use it, and what to do with it when we find it in the wild.
Our objectives for this chapter are three-fold:

  1. Understand how recursion is implemented in a computer and translate this into a model for how to think about recursive functions.

  2. Use recursion as a problem solving technique, recognizing the role of "subproblems" as a primary motivation for recursion.

  3. Be able to analyze the running time of recursive functions.

Here is an example of a recursive function.

```python {cmd, id="j32gqq5q"}
def f(k):
    if k > 0:
        return f(k-1) + k
    return 0

print(f(5))
```

This is actually just our familiar `sumk` function in disguise.
How does it work?
To find the sum of numbers from $1$ to $k$, it just finds the sum of the numbers from $1$ to $k-1$ and then adds $k$.
Yes, we know there is a better way to compute this sum, but there is something satisfying about this approach.
We were asked to solve a problem given some input $k$ and we pretended we already had a solution for smaller numbers ($k-1$ in this case).
Then, we used that solution to construct a solution for $k$.
The magic comes from the fact that the "pretended" solution was actually the same function.
I call this the *pretend someone else wrote it* approach to recursion.
It's very handy for both writing and analyzing recursive functions.



## Recursion and Induction

The function `f` above does the same thing as our `sumk` function that we saw earlier.
You can check it using something called induction.
In fact, this checking process is exactly what it means to "do a proof by induction".
There, you prove a fact, by checking that it is true in the base case.
Then, you prove that it's true for `k` assuming it's true for `k-1`.
In the special case of checking that our function `f` is identical to the `sumk` function that simply returns $\frac{k(k+1)}{2}$, it looks as follows.
First, check that indeed

\[
  f(0) = 0 = \frac{0 * (0 + 1)}{2}.
\]

Then observe that
\[
    f(k) = f(k-1) + k = \frac{(k-1)(k-1 + 1)}{2} + k = \frac{(k-1)k + 2k}{2} = \frac{k(k+1)}{2}.
\]

We won't get many opportunities to do such proofs in this class, but it's worth remembering that there is a strong connection between recursion and induction and working through this connection can enrich your understanding of both concepts.

## Some Basics

Here are some basic rules that you should try to follow to make sure your recursive algorithms terminate.

  1. Have a base case.  If every function call makes another recursive call, you will never terminate.
  2. Recursive calls should move towards the base case.  This usually means that the recursive calls are made on "smaller" subproblems.  Here, "smaller" can mean different things.

It's not hard to write a recursive function that never stops *in theory*.
However, in practice, so-called infinite recursion is pretty quickly discovered with a `RecursionError`.
Python has a limit on the recursion depth.
This limit is usually around 1000.

## The Function Call Stack

To think clearly about recursion, it helps to have an idea of how recursion works on a real computer.
It is easiest to first understand how all function calls work and then it should be clear that there is no technical difference in making a recursive function call compared to any other function call.

```python {cmd id="j32h294n"}
def f(k):
    var = k ** 2
    return g(k+1) + var

def g(k):
    var = k + 1
    return var + 1

print(f(3))
```

The following code gives a `RecursionError` even though none of the functions call themselves directly.
The error is really just signaling that the call stack reached its limit.

```python
def a(k):
    if k == 0: return 0
    return b(k)

def b(k):
    return c(k)

def c(k):
    return a(k-1)

a(340)
```

An interesting recursive example con be constructed by creating two lists, each one containing the other.

```python {cmd}
A = [2]
B = [2]
A.append(A)
B.append(B)
A == B
```

In this case, the recursive function is `list.__eq__`, the method that compares two lists when you use `==`.  It compares the list by checking if the elements are equal.  The lists `A` and `B` each have length 2.  The first elements match.  The second element of each list is another list.  To compare them, there is another call to `list.__eq__`.  This is a repeat of the first call and the process repeats until the recursion limit is reached.

## The Fibonacci Sequence

Here is a classic example of a recursively defined function.
It was originally named for Leonardo Fibonacci who studied it in the context of predicting the growth of rabbit populations.

```python {cmd id="j32h6rso"}
def fib(k):
    if k in [0,1]: return k
    return fib(k-1) + fib(k-2)

print([fib(i) for i in range(15)])
```

This works, but it starts to get really slow, even for small values of `k`.
For example, I tried to run it for `k = 40` and gave up on it.

This is a case that we will encounter many times in this course.
Once we embrace recursion as a way to think about breaking problems into smaller pieces, we may find very short recursive algorithms, but for one reason or another, we may want to rewrite them without recursion.
Here's a version that uses a loop instead.

```python {cmd id="j32hgrm1"}
def fib(k):
    a, b = 0,1
    for i in range(k):
        a, b = b, a + b
    return a

print(fib(400))
```

This is much better!
At first look, it might seem like the only difference in the total work is just in the extra overhead of making function calls rather than updating local variables.
This is wrong.
Let's work out in more detail exactly what function calls are made in the recursive implementation.
Let's say we called `fib(6)`.
This makes calls to `fib(5)` and `fib(4)`.
This, in turn makes calls to `fib(4)` and `fib(3)` as well as `fib(3)` and `fib(2)`.
Each of these four function calls will make two more function calls each.
We can draw them out in a tree.
Notice, that already, we have multiple calls to `fib(4)` as well as to `fib(3)`.
We might as well ask, how many times will we call the same function with the same value?
If we compute `fib(k)`, the answer, interestingly enough is related to the Fibonacci numbers themselves.
Let $T(k)$ denote the number of calls to `fib` when computing `fib(k)`.
It's easy to see that $T(k) = T(k-1) + T(k-2) + 1$.
In this case, the result is nearly exactly the Fibonacci numbers ($T(1) = 1$, $T(2) = 2$, $T(3) = 4$, $T(4) = 7$, ...).  In each case, the value of $T$ is one less than a Fibonacci number.  Thus, the running time of `fib` will grow like the Fibonacci numbers, or equivalently, it will grow like ideal rabbit families, exponentially.  The $k$th Fibonacci number is about $\phi^k$, where $\phi = \frac{1+\sqrt{5}}{2}\sim1.618$ is known as the Golden Ratio.

## Euclid's Algorithm

Euclid's algorithm is a classic in every sense of the word.
The input is a pair of integers `a, b` and the output is the greatest common divisor, i.e., the largest integer that divides both `a` and `b` evenly.
It is a very simple recursive algorithm.
We'll look at the code first and then try to figure out what its doing, why it works, and how we can improve it.

```python
def gcd(a, b):
    if a == b:
        return a
    if a > b:
        a, b = b, a
    return gcd(a, b - a)
```

Like all recursive algorithms, there is a base case.
Here, if `a == b`, then `a` (or equivalently, `b`) is the answer and we return it.
Otherwise, we arrange it so `a < b` and make a recursive call: `gcd(a, b - a)`.

When we walk through some examples, by hand, it seems like the algorithm makes many recursive calls when `b` is much bigger than `a`.
In fact, it's not hard to see that we'll need at least `a // b` recursive calls before we swap `a` and `b`.
These calls are just repeatedly subtracting the same number until it gets sufficiently small.
This is known to elementary school students as division.
This is actually a deep idea that's worth pondering.  Division is iterated subtraction the same way that multiplication is iterated addition, exponentiation is iterated multiplication, and logarithms are iterated division.
Theoretical computer scientists even have a use for iterated logarithms (we call it $\log^\star$, pronounced "log star").

We can just do the division directly rather than repeatedly subtracting the smaller from the bigger.
The result is a slight change to the base case and replacing the subtraction with the modulus operation.
Here is the revised code.

```python {cmd id="j32hniri"}
def gcd(a, b):
    if a > b:
        a, b = b, a
    if a == 0:
        return b
    return gcd(a, b % a)

print("GCD of 12 and 513 is", gcd(12, 513))
print("GCD of 19 and 513 is", gcd(19, 513))
print("GCD of 19 and 515 is", gcd(515 ,19))
```

Incidentally, if `a` and `b` are allowed to be arbitrary numbers, you might try find examples where the gcd algorithm gets caught in an infinite recursion.  In this way, you might discover the irrational numbers.  If `a` and `b` are rational, then the algorithm is also guaranteed to terminate.

If you wanted to find an example that was as bad as possible, you might try to find a pair `(a,b)` such that after one iteration, you get the pair `(b-a, a)` where the ratio of the numbers is the same.  Then, you can check that this will continue and therefore, you'll never get closer to that base case.  But is that possible?  Is there a pair of numbers with this property?  The answer is yes.  One could use $a = 1$ and $b = \phi$, the Golden Ratio.

<!-- ## Removing Recursion

In the Fibonacci example, we got a big improvement -->
