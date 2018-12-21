# Iterators, Generators, and Comprehensions

## For loops and comprehensions, the long way.

The simplest way to make a `list` is to just write out the elements inside square brackets, as follows.

```python
L = [1, 2, 4, 8, 16]
```

This is called a **list literal**.  Often, we want to create a list and we know exactly what items we want to put in it.
However, even in some of these situations, it might not be so nice to write out all the elements.  In the example above, we have the first five powers of two, but what if we needed a list of the first 1000 powers of two.  We might build it up with a for loop.

```python {cmd=true}
L = []
for i in range(1000):
    L.append(2 ** 1)
```

That’s easy enough, but there is an easier syntax for doing this.  It’s called a **list comprehension**.  It looks a little like a for loop inside square brackets:

```python {cmd}
L = [2 ** i for i in range(1000)]
```

This is a very common idiom used in all kinds of programs.  You can do comprehensions with other types of collections too.  For example the following **set comprehension** is equivalent to a for loop construction as follows.

```python {cmd}
S = {(i, i + 1) for i in [4, 5, 6]}
print(S)

S = set()
for i in [4, 5, 6]:
    S.add((i, i + 1))
print(S)
```

Both snippets of code produce the same set of pairs.

## More exotic comprehensions

More complicated comprehensions are possible.  If you want to have nested loops, that is possible; just keep the loops in the same order you would write them if you were writing them out the long way.

```python {cmd}
L = [(i + j + 2) for i in range(5) for j in range(5)]
print(L)

# ... is equivalent to ...

L = []
for i in range(5):
    for j in range(5):
        L.append(i + j + 2)
print(L)
```

## Iterators

The `for` loop is a powerful tool for working with lists, tuples, sets, strings, and dictionaries.
It is the basic way that we loop over a collection.
In this chapter, we’ll delve deeply into how it really works.
At the heart of a `for` loop is the notion of an **iterator**.
The job of an iterator is to provide sequential access to objects in a collection.

The reason we need a separate object to iterate over a list is that we need that object to keep track of where in the list we are.  If we imagine the list written out on a piece of paper.  If we read out the items in the list in order, we might keep our finger on the current item.  Our finger is acting as the iterator’s internal state, keeping our place in the list.  The same is true for other iterators.

The simplest way to get an iterator object is to call the `iter` method on some collection, such as a list.  Internally Python calls the `__iter__` method on the object.

```python {cmd}
L = [2,4,6]
myiterator = iter(L)
```

Any object for which we can call `iter` is called **iterable**.  It is not uncommon to use iterable as a noun as well, saying the object or class is an iterable.  This slight abuse of grammar is consistent with the **is a** vocabulary used in duck typing.  It has the ``__iter__`` method and therefore it *is iterable*.

Once you have an iterator, you can access the items by calling the `next` function as follows.  Internally, Python calls the `__next__` method on the iterator.

```python {cmd}
item = next(myiterator)
```

Any iterable for which you can call `next` in this way is an iterator.  Again, this is duck typing at work.  If the class has an `__iter__` and `__next__` method, then it is an iterator.

If there are no more items, the `next` function will raise the `StopIteration` exception.

```python {cmd}
emptyiterator = iter([])
next(emptyiterator)
```


When you use these collections in a `for` loop, the first thing Python does is call `iter` on them to get an iterator.   You can rewrite a `for` loop with a `while` loop as follows.

```python {cmd}
L = [1,1,2,3,5,8]

for f in L:
    print(f)

# is equivalent to

myiterator = iter(L)
while True:
    try:
        f = next(myiterator)
    except StopIteration:
        break
    print(f)
```

Everyone agrees that the `for` loop is much prettier and easier to understand.  However, the `while` loop version doesn’t hide anything (or at least not as much).  You should never write a `while` loop like the one above, but you should understand it.  That is how you’ll know what is really happening in a `for` loop and someday it will help you track down a bug.  It’s also how you would understand the running time of a `for` loop.

In Python, an iterator is required to also be iterable.  That is, I should be able to call `iter` on an iterator and get an iterator; usually this just gives me back the same iterator.  This is very useful, because it means that there is no problem if I try to loop over an iterator.  The following code works.

```python {cmd}
L = [1,2,3,5,7,11]
for i in iter(L):
    print(i)
```

You should think of the iterator as a separate object from the object it is iterating over.  It keeps track of where it is in the list.  This is why you can have multiple iterators over the same collection at the same time.

```python {cmd}
L = [3, 5, 8]
for i in L:
    for j in L:
        print(i, j)
```

The builtin function `iter` calls the `__iter__` magic method on the object.  The builtin function `next` calls the `__next__` method.  So, you can create your own iterators objects and your own iterable objects by implementing these methods.  We’ll see examples a little later.

## Generators

A **generator** is an easy way to write your own iterators in Python.  It looks like a function, but it includes one or more `yield` statements.  When called, it will return an object of type generator.  A generator is  an iterator, i.e. you can call `next` and `iter` on it.  This also mean you can loop over it.

Because a generator is an iterator, you can imagine that calling `next` should execute the function until the first value is yielded, and then it pauses.  Calling next again will cause the execution to continue from where it left off.  If the function returns, then `StopIteration` will be raised.  

```python {cmd}
def mygen(k):
    for i in range(k):
        yield 2 ** i

for poweroftwo in mygen(4):
    print(poweroftwo)

myiterator = mygen(8)
print(next(myiterator))
print(next(myiterator))
print(next(myiterator))
```

Above we have a simple generator.  It is used in a `for` loop and it is also used explicitly with the `next` function.  You should understand the function call `mygen()` as returning an iterator.  The type of the iterator object is `generator`.  Because we’ve already seen that the generator is an iterator, we know this means that `__iter__` and `__next__` are defined on the generator and so we can call `iter` and `next` respectively.

## Generator Expressions and Comprehensions

It very often happens that we want to create our

```python {cmd}
class MyCollection:
    def __iter__(self):
        for i in range(5):
            yield i + 1000

print(list(enumerate(MyCollection(), start=10)))
```

```python {cmd}
def mymax(S):
    items = iter(S)
    max = next(items)
    for item in items:
        if item > max:
            max = item
    return max

print(mymax([2,5,1]))
```

```python {cmd}
def mysum(S):
    items = iter(S)
    sum = next(items)
    for item in items:
        sum += item
    return sum
```

```python {cmd}
def up(S, f):
    items = iter(S)
    output = next(items)
    for item in items:
        output = f(output, item)
    return output

L = [2,1,5,3,4]
print(up(L, lambda a,b: a if a > b else b))

print(up(L, lambda a,b: a+b))
```

```python {cmd}
def myreduce(f):
    def up(S):
        items = iter(S)
        output = next(items)
        for item in items:
            output = f(output, item)
        return output
    return up

mymax = myreduce(lambda a,b: a if a > b else b)
mysum = myreduce(lambda a,b: a + b)
myall = myreduce(lambda a,b: a and b)

L = [2,1,5,3,4]
print(mymax(L))
print(mysum(L))
print(myall(i < 5 for i in L))
print(myall(i < 6 for i in L))
```


```python {cmd}
from itertools import permutations
print(set(''.join(w) for w in permutations("wow")))
```
