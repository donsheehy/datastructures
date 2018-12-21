# Mappings and Hash Tables

A **mapping** is an association between two sets of things.  It associates a value to a key.  We  refer to these associated pairs as **key-value pairs**.
Keys must be unique, so that there can only be one value associated with a given key.

The standard built-in data type in python for mappings is the dictionary (`dict`).
This kind of mapping is used by python itself to associate names of variables (strings) with objects.
In the notation for dictionaries, we would write `d[some_key] = some_value`.
This either creates a new key-value pair if `some_key` was not already in the dictionary, or it overwrites the existing pair with key `some_key`.

Not all programming languages come with a built-in data type for mappings.
We're going to pretend for a short time that we don't have a python dictionary available to us and go through the process of implementing one ourselves.  This will allow us to resolve one of the major unsolved mysteries from earlier in the course:

> Why does accessing or assigning a value in a dictionary take only constant time?

## The Mapping ADT

A **mapping** is a collection of key-value pairs such that the keys are unique (i.e. no two pairs have the same key).
It supports the following methods.

  - **`get(k)`** - return the value associate to the key `k`.  Usually an error (`KeyError`) is raised if the given key is not present.

  - **`put(k, v)`** - Add the key-value pair `(k,v)` to the mapping.

These are the two main operations.  They are what make a mapping, and are generally implemented as `__getitem__` and `__setitem__` in python in order to support the familiar square bracket notation.  We will put off anything more elaborate for now.  When we get into some implementations, we will put some other conditions on the keys.

## A minimal implementation

Here is a very lightweight method for using a `list` as a mapping.  We start with a little class to store key-value pairs, then give two methods to implement get and put.

```python {cmd id="_trivialmapping"}
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return str(self.key) + " : " + str(self.value)

def mapput(L, key, value):
    for e in L:
        if e.key == key:
            e.value = value
            return
    L.append(Entry(key, value))

def mapget(L, key):
    for e in L:
        if e.key == key:
            return e.value
    raise KeyError
```

```python {cmd continue="trivialmapping"}
m = []
mapput(m, 4, 'five')
mapput(m, 1, 'one')
mapput(m, 13, 'thirteen')
mapput(m, 4, 'four')
assert(mapget(m, 1) == 'one')
assert(mapget(m, 4) == 'four')
```

At this point, it seems that the only advantage of the `dict` structure is that it provides some useful syntax for adding and getting entries.  There are some other advantages, but we'll only reveal them by trying to build a map ourselves.

First, let's put our new data structure in a class.  This will allow us to encapsulate the underlying list so that users don't accidentally mess it up, for example, by appending to it rather than using `put`.  We'd like to protect users from themselves, especially when there are properties of the structure we want to maintain.  In this case, we want to make sure keys stay unique.

```python {cmd id="_listmappingsimple"}
class ListMappingSimple:
    def __init__(self):
        self._entries = []

    def put(self, key, value):
        for e in self._entries:
            if e.key == key:
                e.value = value
                return
        self._entries.append(Entry(key, value))

    def get(self, key):
        for e in self._entries:
            if e.key == key:
                return e.value
        raise KeyError
```

This is an okay start.  It supports `get` and `put` and that's enough to be a mapping, but we'd like several more interesting methods to really put such a structure to use.  Let's extend the ADT with more features.

## The extended Mapping ADT

As with any collection, we might want some other methods such as `__len__`, `__contains__`, or various iterators.  

The standard behavior for iterators in dictionaries is to iterate over the keys.  Alternative iterators are provided to iterate over the values or to iterate over the key-value pairs as tuples.  For a `dict` object this is done as follows.

```python {cmd}
d = {'key1': 'value1', 'key2': 'value2'}

for k in d:
    print(k)

for v in d.values():
    print(v)

for k, v in d.items():
    print(k, v)
```

We'll add the same kind of functionality to our Mapping ADT.  So, the **extended Mapping ADT** includes the following methods (with get and put renamed for python magic).

  - `__getitem__(k)`** - return the value associate to the key `k`.  Usually an error (`KeyError`) is raised if the given key is not present.

  - `__setitem__(k, v)` - Add the key-value pair `(k,v)` to the mapping.

  - `__len__` - return the number of keys in the dictionary.

  - `__contains__(k)` - return true if the mapping contains a pair with key `k`.

  - `__iter__` - return an iterator over the keys in the dictionary.

  - `values` - return an iterator over the values in the dictionary.

  - `items` - return an iterator over the key-value pairs (as tuples).

It is very important to recall from the very beginning of the course that the `dict` class is a **non-sequential collection**.  That is, there is no significance to the ordering of the items and furthermore, you should never assume to know anything about the ordering of the pairs.  You should not even assume that the ordering will be consistent between two iterations of the same `dict`.  This same warning goes for the mappings we will implement and we'll see that the ability to rearrange the order of how they are stored is the secret behind the mysteriously fast running times.  However, this first implementation will have the items in a fixed order because we are using a `list` to store them.

```python {cmd id="_listmapping_notDRY"}
class ListMapping:
    def __init__(self):
        self._entries = []

    def put(self, key, value):
        e = self._entry(key)
        if e is not None:
            e.value = value
        else:
            self._entries.append(Entry(key, value))

    def get(self, key):
        e = self._entry(key)
        if e is not None:
            return e.value
        else:
            raise KeyError

    def _entry(self, key):
        for e in self._entries:
            if e.key == key:
                return e
        return None

    def __str__(self):
        return str([str(e) for e in self._entries])

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __len__(self):
        return len(self._entries)

    def __contains__(self, key):    
        if self._entry(key) is None:
            return False
        else:
            return True

    def __iter__(self):
      return (e.key for e in self._entries)

    def values(self):
        return (e.value for e in self._entries)

    def items(self):
        return ((e.key, e.value) for e in self._entries)
```

Note that I took the opportunity to factor out some duplication in the `get` and `put` methods.

## It's Too Slow!

Our goal is to to get the same kind of constant-time operations as in the `dict` class.  Right now, we are very far from that.  Currently, we need linear time to get put, and check membership.  To do better, we're going to need a new idea.  The `ListMapping` takes linear time because it has to iterate through the list.  We could make this faster if we had many short lists instead of one large list.  Then, we just need to have a quick way of knowing which short list to search or update.  

We're going to store a list of `ListMappings`.
For any key `k`,  we want to compute the index of the *right* `ListMapping` for `k`.  We often call these `ListMapping`s *buckets*.  This term goes back to the idea that you can quickly group items into buckets.  Then, when looking for something in a bucket, you can check all the items in there assuming there aren’t too many.

This means, we want an integer, i.e. the index into our list of buckets.  A **hash function** takes a key and returns an integer.  Most classes in python implement a method called `__hash__` that does just this.  We can use it to implement a simple mapping scheme that improves on the `ListMapping`.  

```python {cmd id="_hashmappingsimple"}
class HashMappingSimple:
    def __init__(self):
        self._size = 100
        self._buckets = [ListMapping() for i in range(self._size)]

    def __setitem__(self, key, value):
        m = self._bucket(key)
        m[key] = value

    def __getitem__(self, key):
        m = self._bucket(key)
        return m[key]

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]
```

Let's look more closely at this code.  It seems quite simple, but it hides some mysteries.

First, the initializer creates a list of 100 ListMaps.  These are called the buckets. If the keys get spread evenly between the buckets then this will be about 100 times faster!  If two keys are placed in the same bucket, this is called a **collision**.

The `__getitem__` and `__setitem__` methods call the `_bucket` method to get one of these buckets for the given key and then just use that ListMap's get and put methods.  So, the idea is just to have several list maps instead of one and then you just need a quick way to decide which to use.  The `hash` function returns an integer based on the value of the given key.  The collisions will depend on the hash function.

### How many buckets should we use?

The number 100 is pretty arbitrary.  If there are many many entries, then one might get 100-fold speedup over ListMap, but not more.  It makes sense to use more buckets as the size increases.  To do this, we will keep track of the number of entries in the map.  This will allow us to implement `__len__` and also grow the number of buckets as needed.  As the number of entries grows, we can periodically increase the number of buckets.  Here is the code.

```python {cmd id="_hashmapping_notDRY"}
from listmapping import ListMapping

class HashMapping:
    def __init__(self, size = 2):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0

    def __setitem__(self, key, value):
        m = self._bucket(key)
        if key not in m:
            self._length += 1
        m[key] = value

        # Check if we need more buckets.
        if self._length > self._size:
            self._double()

    def __getitem__(self, key):
        m = self._bucket(key)
        return m[key]

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]

    def _double(self):
        # Save a reference to the old buckets.
        oldbuckets = self._buckets
        # Double the size.
        self._size *= 2
        # Create new buckets
        self._buckets = [ListMapping() for i in range(self._size)]
        # Add in all the old entries.
        for bucket in oldbuckets:
            for key, value in bucket.items():
                # Identify the new bucket.
                m = self._bucket(key)
                m[key] = value

    def __len__(self):
        return self._length
```

### Rehashing
The most interesting part of the code above is the `_double` method.  This is a method that increases the number of buckets.  It's not enough to just append more buckets to the list, because the `_bucket` method that we use to find the right bucket depends on the number of buckets.  When that number changes, we have to reinsert all the items in the mapping so that they can be found when we next `get` them.  

## Factoring Out A Superclass
We have given two different implementations of the same ADT.  There are several methods that we implemented in the `ListMapping` that we will also want in the `HashMapping`.  It makes sense to avoid duplicating common parts of these two (concrete) data structures.  Inheritance provides a nice way to do this.

This is the most common way that inheritance appears in code.  Two classes want to share some code, so we **factor out a superclass** that both can inherit from and share the underlying code.

There are some methods that we expect to be implemented by the subclass.  We can enforce this by putting the methods in the subclass, but raising an error if they are called.   This way, the error will only be raised if the subclass does not override those methods.

Here is the code for the superclass.

```python {cmd id="_mapping"}
class Entry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __str__(self):
        return "%d: %s" % (self.key, self.value)


class Mapping:

    # Child class needs to implement this!
    def get(self, key):
        raise NotImplemented

    # Child class needs to implement this!
    def put(self, key, value):
        raise NotImplemented

    # Child class needs to implement this!
    def __len__(self):
        raise NotImplemented

    # Child class needs to implement this!
    def _entryiter(self):
        raise NotImplemented        

    def __iter__(self):
      return (e.key for e in self._entryiter())

    def values(self):
        return (e.value for e in self._entryiter())

    def items(self):
        return ((e.key, e.value) for e in self._entryiter())

    def __contains__(self, key):
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.put(key, value)

    def __str__(self):
        return "{%s}" % (", ".join([str(e) for e in self._entryiter()]))
```

There is a lot here, but notice that there are really only four methods that a subclass has to implement: `get`, `put`, `__len__`, and a method called `_entryiter` that iterates through the entries.  This last method is private because the user of this class does not need to access `Entry` objects.  They have the Mapping ADT methods to provide access to the data.  This is why the `Entry` class is an inner class (defined inside the `Mapping` class).

Now, the `ListMapping` can be rewritten as follows.

```python {cmd id="_listmapping"}
from mapping import Mapping, Entry

class ListMapping(Mapping):
    def __init__(self):
        self._entries = []

    def put(self, key, value):
        e = self._entry(key)
        if e is not None:
            e.value = value
        else:
            self._entries.append(Entry(key, value))

    def get(self, key):
        e = self._entry(key)
        if e is not None:
            return e.value
        else:
            raise KeyError

    def _entry(self, key):
        for e in self._entries:
            if e.key == key:
                return e
        return None

    def _entryiter(self):
        return iter(self._entries)

    def __len__(self):
        return len(self._entries)
```

All the magic methods as well as the public iterators and string conversion are handled by the superclass.  The subclass only has the parts that are specific to this implementation.

The `HashMapping` class can also be rewritten as follows.

```python {cmd id="_hashmapping"}
from mapping import Mapping
from listmapping import ListMapping

class HashMapping(Mapping):
    def __init__(self, size = 100):
        self._size = size
        self._buckets = [ListMapping() for i in range(self._size)]
        self._length = 0

    def _entryiter(self):
        return (e for bucket in self._buckets for e in bucket._entryiter())

    def get(self, key):
        bucket = self._bucket(key)
        return bucket[key]

    def put(self, key, value):
        bucket = self._bucket(key)
        if key not in bucket:
            self._length += 1
        bucket[key] = value

        # Check if we need more buckets.
        if self._length > self._size:
            self._double()

    def __len__(self):
        return self._length

    def _bucket(self, key):
        return self._buckets[hash(key) % self._size]

    def _double(self):
        # Save the old buckets
        oldbuckets = self._buckets
        # Reinitialize with more buckets.
        self.__init__(self._size * 2)
        for bucket in oldbuckets:
            for key, value in bucket.items():
                self[key] = value
```
