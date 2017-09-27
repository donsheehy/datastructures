<p style="page-break-after:always;"></p>

# Object-Oriented Programming

A primary goal of **object-oriented programming** is to make it possible to write code that is close to the way you might naturally communicate about the types of things your code is supposed to represent.  This will make it easier to reason about the code and think through its correctness.

A **class** is a data type.  In python *type* and *class* are (mostly) synonymous.  An **object** is an **instance** of a class.  For example, python has a `list` class.  If I make a list called `mylist`.  Then, `mylist` is an object of type `list`.  

```python {cmd=true id="j32a915x"}
mylist = []
print(type(mylist))
print(isinstance(mylist, list))
print(isinstance(mylist, str))
```

There are all kinds of classes built into python.  Some you might not expect.

```python {cmd=true id="j32a89ox"}
def foo():
    return 0

print(type(foo))
```

For the advanced students, here is a more exotic example called a generator.  In python you can `yield` instead of `return`.  If so, the result will be something called a generator and not a function.  This powerful idea shows up a lot in python, but we won't really be able to get our head around it until we understand how classes are able to package up data and code.  

```python {cmd=true id="j32a5vrk"}
def mygenerator(n):
    for i in range(n):
        yield i

print(type(mygenerator))
print(type(mygenerator(5)))
```

## A simple example

One of the first ways that we learn about to combine multiple pieces of information into a single object is in calculus or linear algebra, with the introduction of vectors.  We can think of a 2-dimensional vector as a pair of numbers.  If we are trying to write some code that works with 2-dimensional vectors, we could just use tuples.  It's not too hard to define some basic functions that work with vectors.

```python {cmd=true id="j32a9p9s"}
u = (3,4)
v = (3,6)

def add(a, b):
    return (a[0] + b[0], a[1] + b[1])

def subtract(a,b):
    return (a[0] - b[0], a[1] - b[1])

def dot(a, b):
    return (a[0] * b[0] + a[1] * b[1])

def norm(a):
    return (a[0] * a[0] + a[1] * a[1]) ** 0.5

def isvertical(a):
    return a[0] == 0

print(norm(u))
print(add(u,v))
print(u + v)
print(isvertical(subtract(v, u)))
```

This could be fine if that's all we wanted to do, but as we fill out the code, things will start to get messier.  For example, suppose we want to make sure that the inputs to these functions really are tuples that contain two numbers.  We might add some code to every method to check for this error or recover otherwise, but this is not great, because we really just want to operate on vectors.  Moreover, we might want to `add` other types of things besides vectors.  This would probably require us to make the add function much more complicated, or rename it something more descriptive such as `vectoradd`.

```python {cmd=true id="j32aaa83"}
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

u = Vector(3,4)

print(u.norm())
print(Vector(5,12).norm())
```

A function defined in a class is called a **method**.  It is a standard convention to use `self` as the name of the first parameter to a method.  This parameter is object that will generally be operated on by the method.  When, calling the method, you don't have to pass a parameter explicitly for `self`.  Instead, the dot notation fills in this parameter for you.  That is `u.norm()` is translated into `vector.norm(u)`.  

The `__init__` method is called a **initializer**.  Methods like this one that start and end with two underscores are sometimes called the **magic methods** or also **dunder methods**.  You should not make up your own methods starting and ending with two underscores.  That's how python sets them apart so you don't actually call your own methods the same thing.  Also, dunder methods are usually not called explicitly, but instead provide some other means of calling them.  In the case of a initializer, calling the name of the class as a function invokes the initializer.  You've seen this before, such as in `float("3.14159")`.

We will use another magic method to implement addition.

```python {cmd=true id="j32aaotj"}
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        newx = self.x + other.x
        newy = self.y + other.y
        return Vector(newx, newy)

u = Vector(3,4)
v = Vector(3,6)

print(u + v)
```

That output is pretty weird.  It's telling me that u + v is a vector object at some memory address, but doesn't tell me what vector it is.  We need to implement `__str__` in order to print the vector nicely.  This magic method is called by the print function to convert its parameters into a string.  It is not obvious how a string ought to be printed for a given class.  We have to specify it ourselves.

In the example below, I added an `__str__` method as well as some type checking on the inputs.  The result will guarantee that a vector has two floats as coordinates.

```python {cmd=true id="j32abjfi"}
class Vector:
    def __init__(self, x, y):
        try:
            self.x = float(x)
            self.y = float(y)
        except ValueError:
            self.x = 0.0
            self.y = 0.0

    def norm(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        newx = self.x + other.x
        newy = self.y + other.y
        return Vector(newx, newy)

    def __str__(self):
        return "(%f, %f)" %(self.x, self.y)

u = Vector(3,4)
v = Vector(3,6)

print(u + v)
```
