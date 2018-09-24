# Object-Oriented Programming

```python {cmd hide output="none" id="type02"}
# This is a hack to allow html escape the output of the type function.
import builtins
def type(x):
    return "&lt;" + str(builtins.type(x))[1:-1] + "&gt;"
```

A primary goal of **object-oriented programming** is to make it possible to write code that is close to the way you think about the things your code represents.
This will make it easier to reason about the code and think through its correctness.

A **class** is a data type.  In python *type* and *class* are (mostly) synonymous.  An **object** is an **instance** of a class.  For example, python has a `list` class.  If I make a list called `mylist`.  Then, `mylist` is an object of type `list`.  

```python {cmd id="j32a915x" continue="type02"}
mylist = []
print(type(mylist))
print(isinstance(mylist, list))
print(isinstance(mylist, str))
```

There are all kinds of classes built into python.  Some you might not expect.

```python {cmd id="j32a89ox" continue="type02"}
def foo():
    return 0

print(type(foo))
```

For the advanced students, here is a more exotic example called a generator.  In python you can `yield` instead of `return`.  If so, the result will be something called a generator and not a function.  This powerful idea shows up a lot in python, but we won't really be able to get our head around it until we understand how classes are able to package up data and code.  

```python {cmd id="j32a5vrk" continue="type02"}
def mygenerator(n):
    for i in range(n):
        yield i

print(type(mygenerator))
print(type(mygenerator(5)))
```

## A simple example

One of the first ways that we learn about to combine multiple pieces of information into a single object is in calculus or linear algebra, with the introduction of vectors.  We can think of a 2-dimensional vector as a pair of numbers.  If we are trying to write some code that works with 2-dimensional vectors, we could just use tuples.  It's not too hard to define some basic functions that work with vectors.

```python {cmd id="j32a9p9s"}
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

```python {cmd id="j32aaa83"}
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

```python {cmd id="j32aaotj"}
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

In the example below, I added a `__str__` method as well as some type checking on the inputs.  The result will guarantee that a vector has two floats as coordinates.

```python {cmd id="j32abjfi"}
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

## Encapsulation and the Public Interface of a Class

The word **encapsulation** has two different, but related, meanings.  The first is the idea of encapsulating or combining into a single thing, data and the methods that operate on that data.  In Python, this is accomplished via classes, as we have seen.  

The second meaning of encapsulation emphasizes the boundary between the inside and the outside of the class, specifying what is visible to the users of a class.  Often this means partitioning the attributes into **public** and **private**.  In Python, there is no formal mechanism to keep one from accessing attributes of a class from outside that class.  So, in a sense, everything is public.  However, there is a convention to make it clear what *ought* to be kept private.  Any attribute that starts with an underscore is considered private.  Think of it like someone’s unlocked diary.  You can read it, but you shouldn’t.

```python {cmd id="diary"}
class Diary:
    def __init__(self, title):
        self.title = title
        self._entries = []

    def addentry(self, entry):
        self._entries.append(entry)

    def _lastentry(self):
        return self._entries[-1]
```

In the example above, the `addentry` method is public.  Anyone can add an entry.  However, the `_lastentry` method is private.  One should not call this method from outside of the `Diary` class. (Again, you can, but you shouldn’t.)  The `title` is also public, but the list `_entries` is private.  The collection of all public attributes (in this case, `addentry` and `title`) constitute the **public interface** of the class.  This is what a user of the class should interact with.  For example, one can use the class above as follows.

```python {cmd continue="diary"}
mydiary = Diary("Don’t read this!!!")
mydiary.addentry("It was a good day.")
print("The diary is called ", mydiary.title)
```

Notice that in this example, the encapsulation of the class is not about security.  Heck, if it’s my diary, I should be able to read it, right?  The reason to respect the private attributes and stick to the public interface is really to help us write working code that continues to work in the future.  Code gets changed all the time.  If you are modifying a class that is being used elsewhere in the code, you have to be careful not to break that code.  If the public interface and its behavior doesn’t change, then one can be confident that the changes don’t affect the other code.  One could change the name of a private variable, say changing `_entries` to `_diaryentries` and be confident that this won’t cause some other code somewhere else to break.

## Inheritance and "is a" relationships

Whenever we talk about the types of things in our everyday life, it’s possible to talk about them at different levels of generality.  We can talk about a specific basketball player, say Kylie Irving, or we can talk about professional basketball players, or all basketball players, or people or living creatures.  The specific player we started with could be said to belong to any of these classes.  The same principle applies to code that we write.  

Consider this example from a geometry program.

```python {cmd}
class Triangle:
    def __init__(self, points):
        self._sides = 3
        self._points = list(points)
        if len(self._points) != 3:
            raise ValueError("Wrong number of points.")

    def sides(self):
        return 3

    def __str__(self):
        return "I’m a triangle."

class Square:
    def __init__(self, points):
        self._sides = 4
        self._points = list(points)
        if len(self._points) != 4:
            raise ValueError("Wrong number of points.")

    def sides(self):
        return 4

    def __str__(self):
        return "I’m so square."
```

These are obviously, very closely related classes.  One can make another class for which these two classes are **subclasses**.  Then, anything common between the two classes can be put into the larger class or **superclass**.

```python
class Polygon:
    def __init__(self, sides, points):
        self._sides = sides
        self._points = list(points)
        if len(self._points) != self._sides:
            raise ValueError("Wrong number of points.")		

    def sides(self):
        return self._sides

class Triangle(Polygon):
    def __init__(self, points):
        Polygon.__init__(self, 3, points)

    def __str__(self):
        return "I’m a triangle."

class Square(Polygon):
    def __init__(self, points):
        Polygon.__init__(self, 4, points)

    def __str__(self):
        return "I’m so square."
```

Notice that the class definitions of `Triangle` and `Square` now indicate the `Polygon` class in parentheses.  This is called **inheritance**.  The `Triangle` class **inherits from** (or **extends**) the `Polygon` class.  The **superclass** `Polyon` and the **subclasses** are `Triangle` and `Square`.  When we call a method on an object, if that method is not defined in the class of that object, Python will look for the method in the superclass.   This search for the correct function to call is called the **method resolution order**.   If a method from the superclass is redefined in the subclass, then calling the method on an instance of the subclass calls the subclass method instead.

The initializer of the superclass is not called automatically when we create a new instance (unless we didn’t define `__init__` in the subclass).  In this case, we manually call the `Polygon.__init__` function.  This is one of the few times where it’s acceptable to call a diner method by name.

When using inheritance, you should always remember the most important rule of inheritance:

> Inheritance means **is a**.

This means that if `ClassB` extends `ClassA`, then a `ClassB` object **is a** `ClassA` object.  This should be true at the conceptual level.  So, in our shapes example, we followed this rule, because a triangle is a polygon.  

In total, this might look like more code.  However, it has less duplication.  Duplication is very bad.  Even though it’s easy to copy and paste on a computer, this is a source of many bugs.  The reason is simple.  Bugs are everywhere.  If you copy and paste a code with a bug, then now you have two bugs.  If you find the bug, you have to hope you remember to fix it both places.  Anytime you are relying on your memory, you are going to get yourself in trouble.  

Software engineers use the acronym **DRY**, to mean **Don’t Repeat Yourself**.  They will even use it as an adjective, saying "Keep the code DRY".   The process of removing duplication by putting common code into a superclass is called **factoring out a superclass**.  This is the most common way that inheritance enters a codebase.  Sometimes, opportunities for inheritance are identified at the design stage, before coding begins.

## Duck Typing

Inheritance is considered a staple of object-oriented programming, and it’s important to understand it.  That said, it’s not nearly as useful in Python as it is in other languages.  The reason is that python has built-in (parametric) **polymorphism**.   That means we can pass any type of object we want to a function.  For example, suppose we have a class to store collections of polygons as follows.

```python
class PolygonCollection:
    def __init__(self):
        self._triangles = []
        self._squares = []

    def add(self, polygon):
        if polygon.sides() == 3:
            self._triangles.append(polygon)
        if polygon.sides() == 4:
            self._squares.append(polygon)
```

Notice that the `add` method would work equally well with either version of the `Triangle` and `Square` classes defined previously.  In fact, we could pass it any object that has a method called `sides`.  We didn’t *need* inheritance in order to treat Triangles and squares as special cases of the same object.  Sometimes, inheritance is the right way to combine classes so they can be treated as a single class, but in Python, it’s not as necessary as it is in other languages.

Python’s polymorphism is based on the idea of **duck typing**.  The name comes from an old expression that if something walks like a duck and quacks like a duck, then it *is* a duck.  In the `PolygonCollection` example, if I call the `add` method with an argument that has a `sides` method that returns something that can be compared to an integer, then the code will run without error.  Having the right methods is equivalent to "walking and talking like a duck".  This means that although inheritance should always mean **is a**, not every *“is a”* relationship in your code needs to be expressed with inheritance.  

This idea that *not only inheritance means “is a”* is very important in Python and will be very important throughout this course.  We will discuss this more when we look in more depth at abstract data types.  

One example that we have already seen is the `str` function.  Different types objects can be converted to strings, including objects of classes that we have defined ourselves.  As long as we implemented the `__str__` method on our class, then we can call `str` on an instance of that class.  That function calls the corresponding method, i.e., `str(t)` for a `Triangle` `t` calls `t.__str__()` which is equivalent to `Triangle.__str__(t)`.   

## Composition and "has a" relationships

There are many cases where we want objects of different types to share some functionality.  Sometimes, inheritance is used to allow for this sharing, but more often we use something called **composition**.  This is where one class stores an instance of another class.  It allows us to produce more complex objects.  The most important rule about composition is the following.

> Composition means "has a".

Consider the case where we want a class to behave like a `list`.  For example, we’d like to be able to append to the list and access items by their index, but we don’t want any of the other list stuff.  In this case, it would be *wrong* to use inheritance.  Instead, we would make our class store a list internally (composition).  Then, the public interface to our class would contain the methods we want while making calls to the stored `list` instance to avoid duplicating the list implementation.  Here is an example.

```python {cmd, id="MyLimitedList"}
class MyLimitedList:
    def __init__(self):
        self._L = []

    def append(self, item):
        self._L.append(item)

    def __getitem__(self, index):
        return self._L[index]
```

Here, the magic method `__getitem__` will allow us to use the square bracket notation with our class.  As with other magic methods, we don’t call it directly.

```python {cmd continue="MyLimitedList"}
L = MyLimitedList()
L.append(1)
L.append(10)
L.append(100)
print(L[2])
```
