# Iterators, Generators, and Comprehensions

The `for` loop is a powerful tool for working with lists, tuples, sets, strings, and dictionaries.
It is the basic way that we loop over a collection.
In this chapter, we’ll delve deeply into how it really works.
At the heart of a `for` loop is the notion of an **iterator**.
The job of an iterator is to provide sequential access to objects in a collection.

The simplest way to get an iterator object is to call the `iter` method on some collection, such as a list.

```python {cmd=true}
L = [2,4,6]
myiterator = iter(L)
```

Then, to access the items, you call the `next` function as follows.

```python {cmd=true}
item = next(myiterator)
```

If there are no more items, the `next` function will raise the `StopIteration` exception.

```python {cmd=true}
emptyiterator = iter([])
next(emptyiterator)
```

If you can call `iter` on an object and you get an iterator back, then the object is called **iterable**.

This is all it takes to be iterable or to be an iterator.  We can iterate over basic collections such as lists, tuples, strings, sets, and dictionaries.  These objects are not iterator, but they *are* iterable.  When you use these collections in a `for` loop, the first thing Python does is call `iter` on them to get an iterator.

You can rewrite a `for` loop with a `while` loop as follows.

```python {cmd=true}
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

Everyone agrees that the `for` loop is much prettier and easier to understand.  However, the `while` loop version doesn’t hide anything (or at least not as much).  You should never write a `while` loop like the one above, but you should understand it.  That is how you’ll know what is really happening in a `for` loop and someday it will help you track down a bug.

In Python, an iterator is required to also be iterable.  That is, I should be able to call `iter` on an iterator and get an iterator; usually this just gives me back the same iterator.  This is very useful, because it means that there is no problem if I try to loop over an iterator.  The following code works.

```python {cmd=true}
L = [1,2,3,5,7,11]
for i in iter(L):
	print(i)
```

You should think of the iterator as a separate object from the object it is iterating over.  It keeps track of where it is in the list.  This is why you can have multiple iterators over the same collection at the same time.

```python {cmd=true}
L = [3, 5, 8]
for i in L:
	for j in L:
		print(i, j)
```

The builtin function `iter` calls the `__iter__` magic method on the object.  The builtin function `next` calls the `__next__` method.  So, you can create your own iterators objects and your own iterable objects by implementing these methods.  We’ll see examples a little later.

## Generators
 
A **generator** is an easy way to write your own iterators in Python.  It looks like a function, but it includes one or more `yield` statements.  Because a generator is an iterator, you can imagine that calling `next` should execute the function until the first value is yielded, and then it pauses.  Calling next again will cause the execution to continue from where it left off.  If the function returns, then `StopIteration` will be raised.  

```python {cmd=true}
def mygen():
	for i in range(10):
		yield 2 ** i
		
for poweroftwo in mygen():
	print(poweroftwo)
	
myiterator = mygen()
print(next(myiterator))
```

Above we have a simple generator.  It is used in a `for` loop and it is also used explicitly with the `next` function.  You should understand the function call `mygen()` as returning an iterator.  The type of the iterator object is `generator`.  Because we’ve already seen that the generator is an iterator, we know this means that `__iter__` and `__next__` are defined on the generator and so we can call `iter` and `next` respectively.



```python {cmd=true}
class MyCollection:
    def __iter__(self):
        for i in range(5):
            yield i + 1000

print(list(enumerate(MyCollection(), start=10)))
```

```python {cmd=true}
def mymax(S):
    items = iter(S)
    max = next(items)
    for item in items:
        if item > max:
            max = item
    return max

print(mymax([2,5,1]))
```

```python {cmd=true}
def mysum(S):
    items = iter(S)
    sum = next(items)
    for item in items:
        sum += item
    return sum
```

```python {cmd=true}
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

```python {cmd=true}
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


```python {cmd=true}
from itertools import permutations
print(set(''.join(w) for w in permutations("wow")))
```
