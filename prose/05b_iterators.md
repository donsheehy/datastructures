<p style="page-break-after:always;"></p>

# Iterators, Generators, and Comprehensions

The `for` loop is a powerful tool for working with lists, tuples, sets, strings, and dictionaries.
It is the basic way that we loop over a collection.


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
