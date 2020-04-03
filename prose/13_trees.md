# Trees
```python {cmd id="treedrawings" hide}
from ds2.figs import drawtree
from ds2.tree import Tree
```

```python {cmd figure id="figures.tree_example1" continue="treedrawings" output="html" hide}
T = Tree([1, [2, [3], [4]], [5],[6],[7,[8],[9], [10,[11]]]])
drawtree(T, 'tree_example1')
```

A **Tree** is a data type that is ideal for representing hierarchical structure.
Trees are composed of **nodes** and nodes have $0$ or more **children** or **child nodes**.
A node is called the **parent** of its children.
Each node has (at most) one parent.
If the children are ordered in some way, then we have an **ordered tree**.
We are concerned primarily with **rooted trees**, i.e. there is a single special node called the **root** of the tree.
The root is the only node that does not have a parent.
The nodes that do not have any children are called **leaves** or **leaf nodes**.

There are many many examples of hierarchical (tree-like) structures:

  - Class Hierarchies (assuming single inheritance).  The subclass is the child and the superclasses is the parent.  The Python class `object` is the root.
  - File folders or directories on a computer can be nested inside other directories.  The parent-child relationship encode containment.
  - The tree of recursive function calls in the execution of a divide-and-conquer algorithm.  The leaves are those calls where the base case executes.

Even though we use the family metaphor for many of the naming conventions, a family tree is not actually a tree.  The reason is that these violate the one parent rule.

When we draw trees, we take an Australian convention of putting the root on the top and the children below.  Although this is backwards with respect to the trees we see in nature, it does correspond to how we generally think of most other hierarchies.
Thankfully, there will be sufficiently little conceptual overlap between your experience of trees in the park and the trees in this book, that the metaphoric breakdown should not be confusing.

## Some more definitions

A **path** in a tree is a sequence of nodes in which each node is a child of the previous node.
We say it is a path from $x$ to $y$ if the first node is $x$ and the last node is $y$.
There exists a path from the root to every node in the tree.
The **length of the path** is the number of hops or edges which is one less than the number of nodes in the path.
The **descendants** of a node $x$ are all those nodes $y$ for which there is a path from $x$ to $y$.
If $y$ is a descendant of $x$, then we say $x$ is an **ancestor** of $y$.
Given a tree $T$ and a node $n$ in that tree, the **subtree rooted at $n$** is the tree whose root is $n$ that contains all descendants of $n$.

The **depth** of a node is the length of the path to the node from the root.
The **height** of a tree is the maximum depth of any node in the tree.

This is a lot of definitions to ingest all at once.
It will help to draw some examples and identify check that you can apply the definitions to the examples, i.e. identify the parent, children, descendants, and ancestors of a node.


## A recursive view of trees

A tree can be defined recursively as a root with zero or more children, each of which is tree.
Also, the root of a tree stores some data.
This will be convenient at first and will be important later on as we think about doing more elaborate algorithms on trees, many of which are easiest to describe recursively.
Be warned however, that our object-oriented instincts will later kick in as we separate the notions of trees and nodes.
Having two different kinds of things will lead us to use two different classes to represent them (but not yet).

We can use lists to represent a hierarchical structure by making lists of lists.
To make this a little more useful, we will also store some data in each node of the tree.
We'll use the convention that a list is a tree in which the first item is the data and the remaining items are the children (each should be a list).

Here is a simple example.

```python
['a', ['p'], ['n'], ['t']]
```

This is a tree with `'a'` stored in the root.
The root has 3 children storing respectively, `'p'`, `'n'`, and `'t'`.
Here is a slightly bigger example that contains the previous example as a subtree.

```python {cmd continue="treedrawings" id="tree_example3"}
T = ['c', ['a', ['p'], ['n'], ['t']], ['o', ['n']]]
```

```python {cmd figure continue="tree_example3" id="figures.tree_example3" hide output=html}
drawtree(T, 'tree_example3')
```


We can print all the nodes in such a tree with the following code.

```python {cmd continue="tree_example3"}
def printtree(T):
    print(T[0])
    for child in range(1, len(T)):
        printtree(T[child])

printtree(T)
```

Whenever I see code like that above, I want to replace it with something that can work with any iterable collection.
This would involve getting rid of all the indices and using an iterator.  Here's the equivalent code that uses an iterator.

```python {cmd continue="tree_example3"}
def printtree(T):
    iterator = iter(T)
    print(next(iterator))
    for child in iterator:
        printtree(child)

printtree(T)
```

Here we use the iterator to extract the first list item, then loop through the rest of the children.
So, when we get to the `for` loop, the iterator has already yielded the first value and it will start with the second, i.e., the first child.


## A Tree ADT

The information in the tree is all present in the *list of lists* structure.
However, it can be cumbersome to read, write, and work with.
We will package it into a class that allows us to write code that is as close as possible to how we think about and talk about trees.
As always, we will start with an ADT that describes our expectations for the data structure and its usage.
The **Tree ADT** is as follows.

- **`__init__(L)`** : Initialize a new tree given a list of lists.  The convention is that the first element in the list is the data and the later elements (if they exist) are the children.

- **`height()`** : Return the height of the tree.

- **`__str__()`** : Return a string representing the entire tree.

- **`__eq__(other)`** : Return `True` if the tree is equal to `other`.  This means that they have the same data and their children are equal (and in the same order).

- **`__contains__(k)`** : Return `True` if and only if the tree contains the data `k` either at the root or at one of its descendants.  Return `False` otherwise.

- **`preorder()`** Return an iterator over the data in the tree that yields values according to the **preorder** traversal of the tree.

- **`postorder()`** : Return an iterator over the data in the tree that yields values according to the **postorder** traversal of the tree.

- **`__iter__()`** : An alias for preorder.

- **`layerorder()`** : Return an iterator over the data in the tree that yields values according to the **layer order** traversal of the tree.


## An implementation

```python {cmd id="_tree.tree" hide}
from ds2.queue import ListQueue as Queue
```

```python {cmd id="_tree.tree_00" continue="_tree.tree"}
class Tree:
    def __init__(self, L):
        iterator = iter(L)
        self.data = next(iterator)
        self.children = [Tree(c) for c in iterator]
```

The initializer takes a *list of lists* representation of a tree as input.  A `Tree` object has two attributes, `data` stores data associated with a node and `children` stores a list of `Tree` objects.
The recursive aspect of this tree is clear from the way the children are generated as `Tree`'s.  This definition does not allow for an empty tree (i.e. one with no nodes).

Let's rewrite our print function to operate on an instance of the `Tree` class.

```python {cmd id="printfunction2" continue="_tree.tree_00"}
def printtree(T):
    print(T.data)
    for child in T.children:
        printtree(child)
```

```python {cmd continue="printfunction2"}
T = Tree(['a', ['b', ['c', ['d']]],['e',['f'], ['g']]])
printtree(T)
```

This is the most common pattern for algorithms that operate on trees.
It has two parts; one part operates on the data and the other part applies the function recursively on the children.

One unfortunate aspect of this code is that although it prints out the data, it doesn't tell us about the structure of the tree.
It would be nicer if we used indentation to indicate the depth of the node as we print the data.
It turns out that this is not too difficult and we will implement it as our `__str__` method.

```python {cmd id="treetostring1" continue="_tree.tree_00"}
    def __str__(self, level = 0):
        treestring = "  " * level + str(self.data)
        for child in self.children:
            treestring += "\n" + child.__str__(level + 1)
        return treestring
```

```python {cmd continue="treetostring1"}
T = Tree(['a', ['b', ['c', ['d']]],['e',['f'], ['g']]])
print(str(T))
```

To "see" the tree structure in this print out, you find the parent of a node by finding the lowest line above that node that is not at the same indentation level.
This is a task that you have some training for; it is how you visually parse Python file to understand their block structure.


Although the code above seems to work, it does something terrible.
It builds up a string by iterative adding more strings (i.e. with concatenation).
This copies and recopies some part of the string for every node in the tree.
Instead, we would prefer to just keep a nice list of the trees and then join them into a string in one final act before returning.
To do this, it is handy to use a helper method that takes the level and the current list of trees as parameters.
With each recursive call, we add one to the level, and we pass down the same list to be appended to.


```python {cmd id="_tree.tree_01" continue="_tree.tree_00"}
    def _listwithlevels(self, level, trees):
        trees.append("  " * level + str(self.data))
        for child in self.children:
            child._listwithlevels(level + 1, trees)

    def __str__(self):
        trees = []
        self._listwithlevels(0, trees)
        return "\n".join(trees)
```

```python {cmd continue="_tree.tree_01"}
T = Tree(['a', ['b', ['c', ['d']]],['e',['f'], ['g']]])
print(str(T))
```

The pattern involved here is called a tree traversal and we will discuss these in more depth below.
We implemented this one first, because it will help us to see that our trees look the way we expect them to.
Naturally, it is vital to write good tests, but when things go wrong, you can learn a lot by seeing the tree.
It can give you hints on where to look for bugs.

Here is another example of a similar traversal pattern.
Let's check if two trees are equal in the sense of having the same shape and data.  We use the `__eq__` method so this method will be used when we use `==` to check equality between `Tree`'s.

```python {cmd id="_tree.tree_02" continue="_tree.tree_01"}
    def __eq__(self, other):
        return self.data == other.data and self.children == other.children
```

Here, it is less obvious that we are doing recursion, but we are because `self.children` and `other.children` are lists and list equality is determined by testing the equality of the items.  In this case, the items in the  lists are `Tree`'s, so our `__eq__` method will be invoked for each one.

Here's another example.  Let's write a function that computes the height of the tree.  We can do this by computing the height of the subtrees and return one more than the max of those.  If there are no children, the height is $0$.

```python {cmd id="_tree.tree_03" continue="_tree.tree_02"}
    def height(self):
        if len(self.children) == 0:
            return 0
        else:
            return 1 + max(child.height() for child in self.children)
```

*Hopefully, you are getting the hang of these generator expressions.*

Recall that the `__contains__` magic method allows us to use the `in` keyword for membership testing in a collection.
The desired behavior of this function as described in the ADT tells us how to implement it.

```python {cmd id="_tree.tree_04" continue="_tree.tree_03"}
    def __contains__(self, k):
        return self.data == k or any(k in ch for ch in self.children)
```

The `any` function takes an iterable of booleans and return `True` if any of them are `True`.
It handles short-circuited evaluation, so it can stop as soon as it finds that one is true.
If the answer is `False`, then this will iterate over the whole tree.
This is precisely the behavior we saw with

## Tree Traversal

Previously, all the collections we stored were either sequential (i.e., `list`, `tuple`, and `str`) or non-sequential (i.e., `dict` and `set`).  The tree structure seems to lie somewhere between the two.
There is some structure, but it's not linear.
We can give it a linear (sequential) structure by iterating through all the nodes in the tree, but there is not a unique way to do this.
For trees, the process of visiting all the nodes is called **tree traversal**.
For ordered trees, there are two standard traversals, called **preorder** and **postorder**, both are naturally defined recursively.

In a preorder traversal, we *visit* the node first followed by the traversal of its children.
In a postorder traversal, we traverse all the children and then visit the node itself.
The *visit* refers to whatever computation we want to do with the nodes.
The `printtree` method given previously is a classic example of a preorder traversal.
We could also print the nodes in a postorder traversal as follows.

```python
def printpostorder(T):
    for child in self.children:
        printpostoder(child)
    print(T.data)
```

It is only a slight change in the code, but it results in a different output.

## If you want to get fancy...

It was considered a great achievement in Python to be able to do this kind of traversal with a generator.  Recursive generators seem a little mysterious, especially at first.  However, if you break down this code and walk through it by hand, it will help you have a better understanding of how generators work.

```python {cmd id="_tree.tree_05" continue="_tree.tree_04"}
    def preorder(self):
        yield self.data
        for child in self.children:
            for data in child.preorder():
                yield data

    # Set __iter__ to be an alias for preorder.
    __iter__ = preorder
```

You can also do this to iterate over the trees (i.e. nodes).  I have made this one private because the user of the tree likely does not want or need access to the nodes.

```python
def _preorder(self):
    yield self
    for child in self.children:
        for descendant in child._preorder():
            yield descendant
```

### There's a catch!

This recursive generator does not run in linear time!
Recall that each call to the generator produces an object.
The object does not go away after yielding because it may need to yield more values.
If one calls this method on a tree, each value yielded is passed all the way from the node to the root.
Thus, the total running time is proportional to the sum of the depths of all the nodes in the tree.
For a degenerate tree (i.e. a single path), this is $O(n^2)$ time.
For a perfectly balanced binary tree, this is $O(n \log n)$ time.

Using recursion and the call stack make the tree traversal code substantially simpler than if we had to keep track of everything manually.
It would not be enough to store just the stack of nodes in the path from your current node up to the root. You would also have to keep track of your place in the iteration of the children of each of those nodes.  Remember that it is the job of an iterator object to keep track of where it is in the iteration. Thus, we can just push the iterators for the children onto the stack too.

```python {cmd id="_tree.tree_06" continue="_tree.tree_05"}
    def _postorder(self):
        node, childiter = self, iter(self.children)
        stack = [(node, childiter)]
        while stack:
            node, childiter = stack[-1]
            try:
                child = next(childiter)
                stack.append((child, iter(child.children)))
            except StopIteration:
                yield node
                stack.pop()					

    def postorder(self):
        return (node.data for node in self._postorder())
```

In the above code, I don’t love the fact that I am reassigning `node` and `childiter` at every iteration of the loop.  Can you fix that so that it still works?

### Layer by Layer

Starting with our non-recursive postorder traversal, we can modify it to traverse the tree layer by layer.
We will consider this traversal when we study heaps later on.

```python {cmd id="_tree.tree_07" continue="_tree.tree_06"}
    def _layerorder(self):
        node, childiter = self, iter(self.children)
        queue = Queue()
        queue.enqueue((node, childiter))
        while queue:
            node, childiter = queue.peek()
            try:
                child = next(childiter)
                queue.enqueue((child, iter(child.children)))
            except StopIteration:
                yield node
                queue.dequeue()					

    def layerorder(self):
        return (node.data for node in self._layerorder())
```
