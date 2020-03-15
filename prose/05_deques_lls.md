# Deques and Linked Lists

A **deque** (pronounced "deck") is a doubly-ended queue.
It acts like both a stack and a queue, storing an ordered collection of items with the ability to add or remove from both the beginning and the end.
Here is the ADT.

## The Deque ADT

  - **addfirst(item)** - add `item` to the front of the deque.
  - **addlast(item)** - add `item` to the end of the deque.
  - **removefirst(item)** - remove and return the first item in the deque.
  - **removelast(item)** - remove and return the last item in the deque.
  - **len** - return the number of items in the deque.


As a start, let's see what a deque implementation would look like using a list.

```python {cmd id="_deque.listdeque"}
class ListDeque:
    def __init__(self):
        self._L = []

    def addfirst(self, item):
        self._L.insert(0, item)

    def addlast(self, item):
        self._L.append(item)

    def removefirst(self):
        return self._L.pop(0)

    def removelast(self):
        return self._L.pop()

    def __len__(self):
        return len(self._L)
```

The code is simple enough, but a couple of operations will start to get slow as the deque gets large.
Inserting and popping at index $0$ takes $O(n)$ time.
This follows from the way lists are stored sequentially in memory.
There is no way to change the beginning of the list without shifting all the other elements to make room or fill gaps.
To make this work, we are going to have to give up on the idea of having the items laid out sequentially in memory.
Instead, we'll store some more information with each item that we can use to extract the order.

## Linked Lists

Linked lists are a simple data structure for storing a sequential collection.
Unlike a standard Python list, it will allow us to insert at the beginning quickly.
The idea is to store the items in individual objects called **nodes**.
A special node is the head of the list.
Each node stores a reference to the next node in the list.

We will use the usual trick of looking back into our intuitive description above to find the nouns that will be the types we will need to define.
In this case, there is the list itself and the nodes.
Let's write a class for a `ListNode`.

```python {cmd id="_deque.linkedlist_00"}
class ListNode:
    def __init__(self, data, link = None):
        self.data = data
        self.link = link
```

Now, to start the `LinkedList`, we will store the head of the list.
We will provide two methods, `addfirst` and `removefirst` both of which modify the beginning of the list.
These will behave roughly like the push and pop operations of the stack.
This first implementation will hide the nodes from the user.
That is, from a users perspective, they can create a linked list, and they can add and remove nodes, but they don't have to touch (or even know about) the nodes.
This is abstraction (hiding details)!

```python {cmd id="simplelinkedlist", continue="_deque.linkedlist_00"}
class LinkedList:
    def __init__(self):
        self._head = None

    def addfirst(self, item):
        self._head = ListNode(item, self._head)

    def removefirst(self):
        item = self._head.data
        self._head = self._head.link
        return item
```

## Implementing a Queue with a LinkedList

Recall that even our best list implementation of a Queue required linear time in the worst case for `dequeue` operations (though constant on average).
We could hope to do better with a linked list.
However, right now, we have no way to add to or remove from the end of the linked list.
Here is an inefficient, though simple and correct way to do it.

```python {cmd id="linkedlist_A" continue="_deque.linkedlist_00"}
class LinkedList:
    def __init__(self):
        self._head = None

    def addfirst(self, item):
        self._head = ListNode(item, self._head)

    def addlast(self, item):
        if self._head is None:
            self.addfirst(item)
        else:
            currentnode = self._head
            while currentnode.link is not None:
                currentnode = currentnode.link
            currentnode.link = ListNode(item)

    def removefirst(self):
        item = self._head.data
        self._head = self._head.link
        return item

    def removelast(self):
        if self._head.link is None:
            return self.removefirst()
        else:
            currentnode = self._head
            while currentnode.link.link is not None:
                currentnode = currentnode.link
            currentnode.link = None
            return currentnode.data
```

```python {cmd hide continue="linkedlist_A"}
LL = LinkedList()
LL.addfirst(3)
LL.addfirst(5)
assert(LL.removefirst() == 5)
LL.addlast(9)
LL.addlast(13)
assert(LL.removefirst() == 3)
assert(LL.removefirst() == 9)
assert(LL.removelast() == 13)
```

The new `addlast` method implements a very common pattern in linked lists.
It starts at the head of the linked list and **traverses** to the end by following the `link`s.
It uses the convention that the `link` of the last node is `None`.

Similarly, `removelast` traverses the list until it reaches the second to last element.

This traversal approach is not very efficient.
For a list of length $n$, we would need $O(n)$ time to find the end.

A different approach might be to store the last node (or **tail**) of the list so we don't have to search for it when we need it.
This requires a bit of overhead to make sure it always stores the correct node.
Most of the special cases happen when there is only one item in the list.
We will be able to use this to get some improvement for `addlast`, because we will be able to jump right to the end without traversing.  We will also be able to clean up the code for `removelast` a little by eliminating the `link.link` stuff and instead just check if we reached the tail.

```python {cmd id="linkedlist_B" continue="_deque.linkedlist_00"}
class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None

    def addfirst(self, item):
        self._head = ListNode(item, self._head)
        if self._tail is None: self._tail = self._head

    def addlast(self, item):
        if self._head is None:
            self.add(item)
        else:
            self._tail.link = ListNode(item)
            self._tail = self._tail.link

    def removefirst(self):
        item = self._head.data
        self._head = self._head.link
        if self._head is None: self._tail = None
        return item

    def removelast(self):
        if self._head is self._tail:
            return self.removefirst()
        else:
            currentnode = self._head
            while currentnode.link is not self._tail:
                currentnode = currentnode.link
            item = self._tail.data
            self._tail = currentnode
            self._tail.link = None
            return item

```

```python {cmd hide continue="linkedlist_B"}
LL = LinkedList()
LL.addfirst(3)
LL.addfirst(5)
assert(LL.removefirst() == 5)
LL.addlast(9)
LL.addlast(13)
assert(LL.removefirst() == 3)
assert(LL.removefirst() == 9)
assert(LL.removelast() == 13)
```


Now we can implement the Queue ADT with a linked list.
It will be surprisingly easy.

```python {cmd id="_queue.linkedqueue"}
# linkedqueue.py
from ds2.deque import LinkedList

class LinkedQueue:
    def __init__(self):
        self._L = LinkedList()

    def enqueue(self, item):
        self._L.addlast(item)

    def dequeue(self):
        return self._L.removefirst()

    def peek(self):
        item = self._L.removefirst()
        self._L.addfirst(item)
        return item

    def __len__(self):
        return len(self._L)

    def isempty(self):
        return len(self) == 0
```

## Storing the length

With our `ListQueue`, we implemented `__len__` to give the number of items in the queue.
To implement the same method on the `LinkedQueue`, we will want **delegate** the length computation to the `LinkedList`.

Let's add the ability to get the length of the linked list.
We'll do it by storing the length and updating it with each operation.

```python {cmd id="_deque.linkedlist_01" continue="_deque.linkedlist_00"}
class LinkedList:
    def __init__(self):
        self._head = None
        self._tail = None
        self._length = 0

    def addfirst(self, item):
        self._head = ListNode(item, self._head)
        if self._tail is None: self._tail = self._head
        self._length += 1

    def addlast(self, item):
        if self._head is None:
            self.addfirst(item)
        else:
            self._tail.link = ListNode(item)
            self._tail = self._tail.link
            self._length += 1

    def removefirst(self):
        item = self._head.data
        self._head = self._head.link
        if self._head is None: self._tail = None
        self._length -= 1
        return item

    def removelast(self):
        if self._head is self._tail:
            return self.removefirst()
        else:
            currentnode = self._head
            while currentnode.link is not self._tail:
                currentnode = currentnode.link
            item = self._tail.data
            self._tail = currentnode
            self._tail.link = None
            self._length -= 1
            return item

    def __len__(self):
        return self._length
```

```python {cmd hide continue="_deque.linkedlist_01"}
LL = LinkedList()
LL.addfirst(3)
LL.addfirst(5)
assert(LL.removefirst() == 5)
LL.addlast(9)
LL.addlast(13)
assert(LL.removefirst() == 3)
assert(LL.removefirst() == 9)
assert(LL.removelast() == 13)
```

We still have to iterate through the whole list in order to remove from the end.
It seems very hard to avoid this.
As a result, our `removelast` method still takes linear time.
We won't fix this until the next chapter and it will require a new idea.
So, instead of testing the deque ADT methods now, we'll instead see how to implement an efficient queue using a linked list.

## Testing Against the ADT

Recall that the Queue ADT specifies the expected behavior of a Queue data structure.
It describes the **public interface** to the class.
Now that we can use our `LinkedList` class to implement a Queue with worst-case constant time operations, we have multiple distinct implementations of the ADT.
Good tests for these data structures would only assume that they implement what is provided in the ADT.
In fact, we probably want to test both implementations with the same tests.

If we rename our first Queue implementations `ListQueue`, we might have had the following tests for it.

```python {cmd error_expected}
import unittest
from ds2.queue import ListQueue

class TestListQueue(unittest.TestCase):
    def testinit(self):
        q = ListQueue()

    def testaddandremoveoneitem(self):
        q = ListQueue()
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 3)

    def testalternatingaddremove(self):
        q = ListQueue()
        for i in range(1000):
            q.enqueue(i)
            self.assertEqual(q.dequeue(), i)

    def testmanyoperations(self):
        q = ListQueue()
        for i in range(1000):
            q.enqueue(2 * i + 3)
        for i in range(1000):
            self.assertEqual(q.dequeue(), 2 * i + 3)

    def testlength(self):
        q = ListQueue()
        self.assertEqual(len(q), 0)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 10)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 20)
        for i in range(15):
            q.dequeue()
        self.assertEqual(len(q), 5)

if __name__ == '__main__':
    unittest.main()
```

Now that we have another implementation, we might be tempted to just copy and paste the old tests, changing the references from `ListQueue` to `LinkedQueue`.
That is a lot of code duplication and code duplication leads to problems.
For example, suppose we realize that our code has issues if we try to `dequeue` from an empty queue.
If we decide on the right behavior, we will enforce it with a test.
Do we also copy the test to the other (copied) test file?
What if one implementation is fixed and the other is not?
When we copy and paste code, we invariably copy and paste bugs.
What was one bug, becomes two bugs.

This is a standard situation where inheritance is called for.
We wanted to copy a bunch of methods to be included in two different classes (`TestListQueue` and `TestLinkedQueue`).
Instead we want them to *share* the methods.
So, we **refactor** the code, by **factoring out a superclass**.
Our new class will be called `TestQueue`.
Both `TestListQueue` and `TestLinkedQueue` will extend `TestQueue`.
Remember extending means inheriting from.

```python {cmd id="_test.testqueue"}
# testqueue.py
class QueueTests:
    def testinit(self):
        q = self.Queue()

    def testaddandremoveoneitem(self):
        q = self.Queue()
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 3)

    def testalternatingaddremove(self):
        q = self.Queue()
        for i in range(1000):
            q.enqueue(i)
            self.assertEqual(q.dequeue(), i)

    def testmanyoperations(self):
        q = self.Queue()
        for i in range(1000):
            q.enqueue(2 * i + 3)
        for i in range(1000):
            self.assertEqual(q.dequeue(), 2 * i + 3)

    def testlength(self):
        q = self.Queue()
        self.assertEqual(len(q), 0)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 10)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 20)
        for i in range(15):
            q.dequeue()
        self.assertEqual(len(q), 5)
```

The new class looks almost exactly the same as our old `TestListQueue` class exactly for a couple small changes.
Instead of creating a new `ListQueue` object in each test, we create a `self.Queue` object.
This may seem strange for two reasons: first, we don't have this class; and second, it is attached to `self` which is the `TestQueue` object.
When we implement the specific tests for each class, we will assign the variable `Queue` to be the class corresponding to the particular implementation we want to test.

There is another *important difference* between the `TestQueue` class and our old `TestListQueue` class---the `TestQueue` class does not extend `unittest.TestCase`.
It just defines some methods that will be **mixed into** `TestListQueue` and `TestLinkedQueue`.
Here are our new test files.

```python {cmd id="_test.testlistqueue" error_expected}
# testlistqueue.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import ListQueue

class TestListQueue(unittest.TestCase, QueueTests):
    Queue = ListQueue

if __name__ == '__main__':
    unittest.main()
```

```python {cmd id="_test.testlinkedqueue" error_expected}
# testlinkedqueue.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import LinkedQueue

class TestListQueue(unittest.TestCase, QueueTests):
    Queue = LinkedQueue

if __name__ == '__main__':
    unittest.main()
```


The classes, `TestListQueue` and `TestLinkedQueue`, extend both `unittest.TestCase` *and* `TestQueue`.
This is called **multiple inheritance**.
In other languages like C++ that support multiple inheritance, it is considered a bad design decision.
However, in Python, it is appropriate to use it for this kind of **mix in**.
The only thing to remember is that the golden rule of inheritance should still be observed: **inheritance mean 'is a'**.


If you wanted to add specific tests to one of these implementations, but not the other, you could do so in the subclasses.
However, if you had many implementations that all should pass the same tests, you might try something like the following pattern.
It creates the test class in a function.
This way, adding tests for a new implementation only takes one line.

```python {cmd id="_test.testbothqueues" error_expected}
# testbothqueues.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import ListQueue, LinkedQueue

def _test(queue_class):
    class QueueTestCase(unittest.TestCase, QueueTests):
        Queue = queue_class
    return QueueTestCase

TestLinkedQueue = _test(LinkedQueue)
TestListQueue = _test(ListQueue)
# TestYetAnotherQueue = _test(YetAnotherQueue)
# TestCrazyOtherQueue = _test(CrazyOtherQueue)

if __name__ == '__main__':
    unittest.main()
```

Notice that ten tests were executed, five for each implementation.
This is the pattern used extensively in the tests for the code in this book.
You are encouraged to look at the code on github and especially the tests.


## The Main Lessons:

  - Use the public interface as described in an ADT to **test** your class.
  - You can use **inheritance** to share functionality between classes.
  - Inheritance means **'is a'**.

## Design Patterns:  The Wrapper Pattern

In the last two chapters, we saw several different implementations of the Queue ADT.
The main ones, `LinkedQueue` and `ListQueue` were very simple.
In both cases, we used **composition**, the class stored an object of another class, and then **delegates** most of the operations to the other class.
These are examples of something called the **Wrapper Pattern**.
The Queue in both cases is a wrapper around another data structure.

**Design patterns** also known as **object-oriented design patterns** or simply **patterns** are ways of organizing classes in to solve common programming problems.
In the case of the Wrapper Pattern, we have a class that already "sort of" does what we want, but it has different names for the operations and it possibly has many other operations that we don't want to support.
So, we create a new class that **has an** instance of another class (a `list` or `LinkedList` in our example) and then provide methods that operate on that object.
From outside the class, we don't have to know anything about the wrapped class.
Sometimes, this separation is called a **layer of abstraction**.
The user of our class does not have to know anything about our implementation in order to use the class.

Here are some of the takeaway lessons:

  - Use design patterns where appropriate to organize your code and improve readability.
  - The Wrapper Pattern gives a way to provide an alternative interface to (a subset of) the methods in another class.
  - Composition means **'has a'**.
