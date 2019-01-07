# Stacks and Queues

## Abstract Data Types

Throughout the book, we will use **abstract data types** or **ADTs** as a starting point for any discussion of a particular data structure.
An ADT is not a data structure, but it does tell us about data structures.
The way we use the term ADT, it will be very similar to the term **interface**.
An ADT answers two main questions:

  1. What is the *data* to be stored or represented?
  2. What can we do with the data?

These together describe the **behavior** or **semantics** of the data structure.
When we give an ADT, we will list the names of the methods that will be present, what kind of input they take, and what is their expected output.
The ADT may also describe error situations and what should happen if they occur.
A **data structure** is an implementation of an ADT.
To make, this distinction, it is sometimes useful to call them **concrete data structures**, though we will usually omit the word "concrete".

The ADT tells us what methods the data structure will implement.
However, the ADT *does not* give an hints or prescriptions for how the data structure is implemented.
This is important both as a definition, but also as a guiding design idea in object-oriented programming, that I will write it again:

> **The ADT should be independent of all concerns about its implementation.**

You may have noticed that the two questions ADTs answer are related to the definition of **encapsulation** we gave in our earlier discussion of object-oriented programming.
As such, when we implement data structures in python, we will package them as classes.

## The Stack ADT
   - **push** - add a new item to the stack.
   - **pop** - remove and return the next item in Last In First Out (LIFO) ordering.
   - **peek** - return the next item in LIFO ordering.
   - **size** - returns the number of items in the stack (we'll use the pythonic `__len__` method)
   - **isempty** - return `True` if the stack has no items and return `False` otherwise.

This ADT can be implemented quite easily using a `list`.
We will implement it with a class called `ListStack`.
Here, we are giving hints about the implementation in the name.
This is more common in Java programming, but we adopt the convention in the book to help us distinguish between different implementations of the same ADT.

```python {cmd id="_liststack_00"}
class ListStack:
    def __init__(self):
        self._L = []

    def push(self, item):
        self._L.append(item)

    def pop(self):
        return self._L.pop()

    def peek(self):
        return self._L[-1]

    def __len__(self):
        return len(self._L)

    def isempty(self):
        return len(self) == 0

```



The `Stack` class above illustrates the object-oriented strategy of *composition* (the `Stack` has a `list`).  It is also an example of the **Wrapper Pattern**.  The Python builtin `list` is doing all the heavy lifting, but from the user's perpective, they don't know or care how the methods are implemented.  This is not exactly true.  The user would start to care if the performance is bad.  It wouldn't be too hard to make this inefficient.  For example, we could have implemented the Stack by pushing new items into the front of the list.  Here we use inheritance to avoid rewriting the methods that will not be changing.

```python {cmd continue="_liststack_00"}
class BadStack(ListStack):    
    def push(self, item):
        self._L.insert(0, item)

    def pop(self):
        return self._L.pop(0)

    def peek(self):
        return self._L[0]

```

A simple asymptotic analysis shows why this implementation is far less efficient.
Inserting a new item into a list requires that all the other items in the list have to move over to make room for the new item.
If we insert at the beginning of the list, then every item has to be copied to a new position.  Thus, the `insert` call in `push` takes $O(n)$ time.
Similarly, if we pop an item at the beginning of the list, then every other item in the list gets moved over one space to fill in the gap.
Thus, the `list.pop` call in our `pop` method will take $O(n)$ time as well.   So, `push` and `pop` both take linear time in this implementation.  It really earns its name.

## The Queue ADT
   - **enqueue** - add a new item to the queue.
   - **dequeue** - remove and return the next item in First In First Out (FIFO) ordering.
   - **len** - returns the number of items in the queue.
   - **isempty** - return `True` if the queue has no items and return `False` otherwise.

```python
class Queue:
    def __init__(self):
        self._L = []

    def enqueue(self, item):
        self._L.append(item)

    def dequeue(self):
        return self._L.pop(0)

    def __len__(self):
        return len(self._L)

    def isempty(self):
        return len(self) == 0
```

"But wait," you say.  "I thought calling `pop(0)` was a bad thing to do."  

Yes, it takes time proportional to the length of the list, but what can we do?  If we dequeue off the end of the list, we would have to enqueue by inserting into the front of the list.  That's bad too.

Here's a different idea.  Let's not really delete things from the front of the list.  Instead, we'll ignore them by keeping the index of the head of the queue.

```python {cmd id="_listqueue_00"}
class Queue:
    def __init__(self):
        self._head = 0
        self._L = []

    def enqueue(self, item):
        self._L.append(item)

    def dequeue(self):
        item = self._L[self._head]
        self._head += 1
        return item

    def __len__(self):
        return len(self._L) - self._head

    def isempty(self):
        return len(self) == 0
```

There is something a little odd about this code: it never gets rid of old items after they have been dequeued.  Even if it deleted them, it still keeps a place in the list for them.  This is a kind of **lazy** update.  Shouldn't we clean up after ourselves?  Yes, but let's wait.  Here's the idea.  If the list ever gets half empty, that is, if `_head` is more than half the length of `_L`, then we will bite the bullet and replace `_L` with a slice of it.  "Biting the bullet" is an especially good turn of phrase here if you view this process as a kind of amputation of the old gangrenous stump of the list.

```python {cmd id="_listqueue_01" continue="_listqueue_00"}
class ListQueue(Queue):
    def dequeue(self):
        item = self._L[self._head]
        self._head += 1
        if self._head > len(self._L)//2:
            self._L = self._L[self._head:]
            self._head = 0
        return item
```

So, it looks like we lost all the benefits of our lazy update, because now we have a `dequeue` method that sometimes takes linear time.  However, we don't do that *every* time.  How expensive is it really?  If we do all our `enqueue` operations first, and then dequeue all our items afterwards, then some items at the end of the list get moved (i.e. copied to a new memory location during the slicing operation) many times.  The first half of the items don't get moved at all.  The next quarter of the list (from $1/2$ to $3/4$) gets moved exactly one time.  The next eighth of the list moves exactly twice.  Of $n$ total items, there are $n/2^i$ items that get moved $i-1$ times.  Thus the total number of moves for $n$ items is at most $n\sum_{i=1}^{\log n} \frac{i-1}{2^i} < n$.  So, "on average",  the cost per item is constant.  

This kind of lazy update is very important.  In fact, it's how python is able to do `list.pop` quickly.  Technically, `pop()` can also take linear time for some calls but on average, the cost is constant per operation.  The same idea makes `append` fast.  In that case, python allocates extra space for the list and every time it fills up, the list is copied to a bigger area, that roughly doubles in size.

## Dealing with errors

Often, we make assumptions about how a class can or ought to be used.
This is also considered part of the semantics of the class and it affects how we program it.
We would like to write error-free code.
We'd like to make it so that it always works no matter how it gets misused, but sometimes, an error message is the correct behavior.

In python we **raise an error** the way one might throw an egg.
Either someone gently catches it or it crashes.
Depending on the situation, either might be the right thing to do.

In the case of a stack, it is never correct usage to `pop` from an empty stack.
Thus, it makes sense that someone using our `Stack` class should have their program crash and see an error message if they attempt to call `pop` when there are no items left on the stack.
In the list implementation above, this does happen:

```python {cmd id="liststackerror" continue="_liststack_00"}
s = ListStack()
s.push(5)
s.pop()
s.pop()
```

If we look at the error message, it even seems pretty good.
It says we tried to `pop from empty list`.
But if you look at the code, you might ask, "What list?"
We know how the `ListStack` class is implemented, and the name even gives a hint at its implementation, so we might guess what's going on, but the user does have to search up the stack trace a little to see the line of their own code that caused the problem.
We could catch the exception in our `pop` method and raise a different error so the source of the problem is more obviously the user's code.
Otherwise, the stack trace reports the error in our code.
Then, a user, might have to try to understand our class in order to backtrack to understand what they did wrong in their code.
Instead, give them an error that explains exactly what happened.

```python {cmd id="anotherstackerror" continue="_liststack_00"}
class AnotherStack(ListStack):
    def pop(self):
        try:
            return self._L.pop()
        except IndexError:
            raise RuntimeError("pop from empty stack")

s = AnotherStack()
s.push(5)
s.pop()
s.pop()
```
