<p style="page-break-after:always;"></p>

# Basic Python

This book is not intended as a first course in programming.
It will be assumed that the reader has some experience with programming.
Therefore, it will be assumed that certain concepts are already familiar to them, the most basic of which is a mental model for programming that is sometimes called *Sequence, Selection, and Iteration*.

## Sequence, Selection, and Iteration

A recurring theme in this course is the process of moving from *thinking about* code to *writing* code.  We will try to shape the way we think about programs, the way we write programs, and how we go between the two in *both* directions.  That is, we want to have facility with both direct manipulation of code as well as high-level description of programs.  
A nice model for thinking about (imperative) programming is called Sequence-Selection-Iteration.  It refers to:
1. **Sequence**: Performing operations one at a time in a specified order.
2. **Selection**: Using conditional statements such as `if` to select which operations to execute.
3. **Iteration**: Repeating some operations using loops or recursion.

In any given programming language, there are usually several mechanisms for selection and iteration, while sequencing is just the default behavior.  
In fact, you usually have to have special constructions in a language to do something other than performing the given operations in the given order.

## Variables, Types,  and State

Imagine you are trying to work out some elaborate math problem without a computer.  
It helps to have paper.
You write things down, so that you can use them later.  It's the same in programming.  It often happens that you compute something and want to keep it until later when you will use it.  We often refer to stored information as **state**.  

We store information in **variables**.  In Python, a variable is created by an **assignment** statement.  That is a statement of the form:

`variable_name = some_value`

The equals sign is doing something (assignment) rather than describing something (equality).

Every variable has a **type**.  The type determines what you can do with the variable.  The so-called **atomic types** in Python are *integers*, *floats*, and *booleans*, but any interesting program will contain variables of many other types as well.  You can inspect the type of a variable using the `type()` function.  In Python, the word *type* and *class* mean the same thing.

Technically, there is a difference between a variable and the **object** it represents.  In our common speech, this distinction gets lost because the variable is usually acting as the *name* of the object.  There are some times when it's useful to be clear about the difference, in particular when copying objects.  You might want to try some examples of copying objects from one variable to another.  Does changing one of them affect the other?

```python {cmd=true id:"j4htmm25"}
x = 5
y = 3.2
z = True
print("x has type", type(x))
print("y has type", type(y))
print("z has type", type(z))
```

In python, you cannot change the type of an object.
You can reassign a variable to point to different object of a different type, but that's not the same thing.
There are several functions that may seem to be changing the types of objects, but they are really just creating a new object from the old.

```python {cmd=true id:"j4htp29r"}
x = 2
print("x =", x)
print("float(x) =", float(x))
print("x still has type", type(x))

print("Overwriting x.")
x = float(x)
print("Now, x has type", type(x))
```

You can do more elaborate things as well.

```python {cmd=true id:"j4htrk52"}
numstring = "3.1415926"
y = float(numstring)
print("y has type", type(y))

best_number = 73
x = str(best_number)
print("x has type", type(x))

thisworks = float("inf")
print("float(\'inf\') has type", type(thisworks))
infinity_plus_one = float('inf') + 1
```

This last example introduced a new type, that of a **string**.  A string is a sequence of characters.  In Python, there is no special class for a single character (as in C for example).
If you want a single character, you use a string of length one.

## Collections

The next five most important types in Python are strings, lists, tuples, dictionaries, and sets.

**Strings** are sequences of characters and can be used to store text of all kinds.  Note that you can **concatenate** strings to create a new string using the plus sign.  You can also access individual characters using square brackets and an **index**.

```python
s = "Hello, "
t = "World."
u = s + t
print(type(u))
print(u)
print(u[9])
```

```
<class 'str'>
Hello, World.
r
```

**Lists** are ordered sequences of objects.  The objects do not have to be the same type.  They are indicated by square brackets and the **elements** of the list are separated by commas.  The `append` method allows you to add to the end of a list.  It is possible to index into a list exactly as we did with strings.

```python
L = [1,2,3]
print(type(L))
L.append(400)
print(L)
```

```python
<class 'list'>
[1, 2, 3, 400]
```

**Tuples** are also ordered sequences of objects, but unlike lists, the objects cannot be changed and it is not possible to append to the end.  We say that tuples are **immutable** whereas lists are not.  Strings are also immutable.

```python {cmd=true id:"j4htlbaj"}
t = (1, 2, "skip a few", 99, 100)
print(type(t))
print(t)
print(t[4])
t.append(101)
```

**Dictionaries** store *key-value* pairs.  That is, every element of a dictionary has two parts, a **key** and a **value**.  If you have the key, you can get the value.  The name comes from the idea that in a real dictionary (book), a word (the key) allows you to find its definition (the value).  Notice that the keys can be different types, but they must be immutable types such as atomic types, tuples, or strings.  The reason for this requirement is that we will determine where to store something using the key.  If the key changes, we will look in the wrong place when it's time to look it up again.

Dictionaries are also known as maps,  **mappings**, or hash tables.  We will go deep into how these are constructed later in the course.

A dictionary doesn't have a fixed order.

```python
d = dict()
d[2] = "two"
d[5] = "five"
d["pi"] = 3.1415926

print(d)
print(d["pi"])
```

```
{'pi': 3.1415926, 2: 'two', 5: 'five'}
3.1415926
```

**Sets** correspond to our notion of sets in math.  They are collections of objects without duplicates.  We use curly braces to denote them and commas to separate elements.  As with dictionaries, a set has no fixed ordering.

Be careful that empty braces `{}` indicates an empty dictionary and not an empty set.

```python
s = {2,1}
print(type(s))
s.add(3)
s.add(2)
s.add(2)
s.add(2)
print(s)
```

```
<class 'set'>
{1, 2, 3}
```

## Some common things to do with collections

There are several operations that can be performed on any of the collections classes (and indeed often on many other types objects).

You can find the number of elements in the collection (the **length**) using `len`.

```python
a = "a string"
b = ["my", "second", "favorite", "list"]
c = (1, "tuple")
d = {'a': 'b', 'b': 2, 'c': False}
e = {1,2,3,4,4,4,4,2,2,2,1}

print(len(a), len(b), len(c), len(d), len(e))
```

```
8 4 2 3 4
```

For the sequential types (lists, tuples, and strings), you can **slice** a subsequence of indices using square brackets and a colon as in the following examples.  The range of indices is half open in that the slice will start with the first index and proceed up to but not including the last index.  Negative indices count backwards from the end.  Leaving out the first index is the same as starting at 0.  Leaving out the second index will continue the slice until the end of the sequence.

**Important**: slicing a sequence creates a new object.  That means a big slice will do a lot of copying.  It's really easy to write inefficient code this way.

```python
a = "a string"
b = ["my", "second", "favorite", "list"]
c = (1, 2,3,"tuple")
print(a[3:7])
print(a[1:-2])
print(b[1:])
print(c[:2])
```

```
trin
 stri
['second', 'favorite', 'list']
(1, 2)
```

## Iterating over a collection

It is very common to want to loop over a collection.
The pythonic way of doing iteration is with a `for` loop.

The syntax is shown in the following examples.

```python
mylist = [1,3,5]
mytuple = (1, 2, 'skip a few', 99, 100)
myset = {'a', 'b', 'z'}
mystring = 'abracadabra'
mydict = {'a': 96, 'b': 97, 'c': 98}

for item in mylist:
    print(item)

for item in mytuple:
    print(item)

for element in myset:
    print(element)

for character in mystring:
    print(character)

for key in mydict:
    print(key)

for key, value in mydict.items():
    print(key, value)

for value in mydict.values():
    print(value)
```

There is class called `range` to represent a sequence of numbers that behaves like a collection.
It is often used in for loops as follows.

```python
for i in range(10):
    j = 10 * i + 1
    print(j,)
```
