# Lambda Expressions and Functional Features of Python

## Functions as Objects

Python allows you to treat a function just like any other object.
This includes assigning a function to a variable, or passing a function.
You can make a list of functions, or even a set of functions.

```python {cmd}
def foo(x):
    return x + 1

a_variable = foo

def bar(a, b = 0):
    return a(b)

print(bar(foo, 5))
print(bar(a_variable, 5))
```

You may have had errors that arise because of this flexibility.
For example, if there is a function that doesn't take any parameters, you might forget to add the parentheses.


```python
def reassureme():
    return "It's going to be just fine, I promise."

print(reassureme)
```

```
<function reassureme at 0x10555b440>
```

This is not so reassuring.  However, once you see that there is a function instead of another type of object, it's not so hard to debug.

Or, a worse situation occurs if you don't get an error.

```python {cmd}
def everythingisokay():
    # Everything is not okay!
    return False

if everythingisokay:
    print("This should not execute.")

# The parentheses will save us.
if everythingisokay():
    haltandcatchfire()
```

In other programming languages, one must engage in some ugly constructions in order to pass a function.
For example, in C++ or Java, it is not uncommon to make a class that has a function so that we can pass an instance of that class in order to get access to the function.

## `key` functions

Perhaps the most common case where one would like to pass a function is in sorting.
By default, sorting will use comparison (`__lt__`) to order items.
If you want a different ordering, or you want to sort points by a

```python {cmd id="point"}
class point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __iter__(self):
        yield self.x
        yield self.y

    def dist(self, other):
        return sum(abs(a - b) for a, b in zip(self, other))

    def __repr__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

P = [point(10,-1), point(2,3), point(3,5)]
```

If we just tried to sort the points, we get an error.

```python {cmd continue="point"}
P.sort()
```

We could define `__lt__`, but it's not obvious that there is a right answer.
We may want different orderings.
For example, we could sort the points by their distance to the origin.

```python {cmd continue="point"}
origin = point(0,0)
P.sort(key = origin.dist)
print(P)
```

You can also use the named parameter `key` in other functions that use orders.
This includes `max` and `min`.

```python {cmd continue="point"}
def nearest(q, S):
    return min(S, key = q.dist)

def farthest(q, S):
    return max(S, key = q.dist)

x = point(3,6)
print("nearest:", nearest(x, P))
print("farthest:", farthest(x, P))
```

## Using lambda functions

Sometimes, we want to define a small function in the middle of something else.
We can use `def` to do this.
Often this is fine.
Here is an example to sort points by their y-coordinate.

```python {cmd continue="point"}
def ycoord(p):
    return p.y

P.sort(key = ycoord)
print(P)
```

This is such a simple function, we might prefer to put the definition right in the function call.
In fact, if we only use the function here, we don't even need to give it a name.
It's name will be `key` when it arrives as an argument to the `sort` function.
Lambda expressions allow us to do just this.
A lambda expression is an expression that evaluates to a function.
Here is an example.

```python
lambda x: x + 1
```

In this case, we can't call this function unless we assign it to a variable.
In the next example, `foo1` and `foo2` do the same thing.

```python {cmd}
foo1 = lambda x: x + 1

def foo2(x):
    return x + 1

for i in range(4):
    print(foo1(i), "==", foo2(i))
```

Now, we can use a lambda expression to sort the points by their y-coordinate.

```python {cmd continue="point"}
P.sort(key = lambda p: p.y)
print(P)
```

We could also sort the sum of the coordinates.

```python {cmd continue="point"}
P.sort(key = lambda p: p.x + p.y)
print(P)
```

You can also have lambda expressions that evaluate to functions with more (or even zero) parameters.

```python {cmd}
foo = lambda : 5
print(foo())

bar = lambda a, b: a * 8 + b
print(bar(1, 2))
print(bar('Na', ' batman'))
```
