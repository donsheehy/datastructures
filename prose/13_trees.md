# Trees

**Trees** data types are ideal for representing hierarchical structure.
Trees are composed of **nodes** and nodes have $0$ or more **children** or **child nodes**.
A node is called the **parent** of its children.
Each node has (at most) one parent.
If the children are ordered in some way, then we have an **ordered tree**.
We are concerned primarily with **rooted trees**, i.e. there is a single special node called the **root** of the tree.
The root is the only node that does not have a parent.
The nodes that do not have any children are called **leaves** or **leaf nodes**.

There are many many examples of hierarchical (tree-like) structures:

  - Class Hierarchies (assuming single inheritance).  The subclass is the child and the superclasses is the parent.  The python class `object` is the root.
  - File folders or directories on a computer can be nested inside other directories.  The parent-child relationship encode containment.
  - The tree of recursive function calls in the execution of a divide-and-conquer algorithm.  The leaves are those calls where the base case executes.

Even though we use the family metaphor for many of the naming conventions, a family tree is not actually a tree.  The reason is that these violate the one parent rule.

When we draw trees, we take an Australian convention of putting the root on the top and the children below.  Although this is backwards with respect to the trees we see in nature, it does correspond to how we generally think of most other hierarchies.

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

## A recursive view of trees

A tree can be defined recursively as a root with $0$ or more children, each of which is tree.
This will be convenient at first and will be important later on as we think about doing more elaborate algorithms on trees, many of which are easiest to describe recursively.
Be warned however, that our object-oriented instincts will later kick in as we separate the notions of trees and nodes.
Having two different kinds of things will lead us to use two different classes to represent them.

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

```python
T = ['c', ['a', ['p'], ['n'], ['t']], ['o', ['n']]]
```

We can print all the nodes in such a tree with the following code.

```python
def printtree(T):
    print(T[0])
    for child in range(1, len(T)):
        printtree(T[child])

printtree(T)
```

Whenever I see code like that above, I want to replace it with something that can work with any iterable collection.
This would involve getting rid of all the indices and using an iterator.  Here's the equivalent code that uses an iterator.

```python
def printtree(T):
    iterator = iter(T)
    print(next(iterator))
    for child in iterator:
        printtree(child)
```

Here we use the iterator to extract the first list item, then loop through the rest of the children.  

The information in the tree is all present in this *list of lists* structure.
However, it can be cumbersome to read, write, and work with.
Let's package this into a class that allows us to write code that is as close as possible to how we think about and talk about trees.

```python
class Tree:
    def __init__(self, L):
        iterator = iter(L)
        self.data = next(iterator)
        self.children = [Tree(c) for c in iterator]
```

The initializer takes a *list of lists* representation of a tree as input.  A `Tree` object has two attributes, `data` stores data associated with a node and `children` stores a list of `Tree` objects.
The recursive aspect of this tree is clear from the way the children are generated as `Tree`'s.

Let's add our print function to the class.

```python
def printtree(self):
    print(self.data)
    for child in self.children:
        child.printtree()
```

This is the most common pattern for algorithms that operate on trees.
It has two parts; one part operates on the data and the other part applies the function recursively on the children.
Here is another example of the same pattern.
Let's check if two trees are equal in the sense of having the same shape and data.  We use the `__eq__` method so this method will be used when we use `==` to check equality between `Tree`'s.

```python
def __eq__(self, other):
    return self.data == other.data and self.children == other.children
```

Here, it is less obvious that we are doing recursion, but we are because `self.children` and `other.children` are lists and list equality is determined by testing the equality of the items.  In this case, the items in the  lists are `Tree`'s, so our `__eq__` method will be invoked for each one.

Here's another example.  Let's write a function that computes the height of the tree.  We can do this by computing the height of the subtrees and return one more than the max of those.  If there are no children, the height is $0$.

```python
def height(self):
    if len(self.children) == 0:
        return 0
    else:
        return 1 + max(child.height() for child in self.children)
```

*Hopefully, you are getting the hang of these generator expressions.*

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
def printpostorder(self):
    for child in self.children:
        child.printpostoder()
    print(self.data)
```

It is only a slight change in the code, but it results in a different output.

## If you want to get fancy...

It was considered a great achievement in python to be able to do this kind of traversal with a generator.  Recursive generators seem a little mysterious, especially at first.  However, if you break down this code and walk through it by hand, it will help you have a better understanding of how generators work.

```python
def preorder(self):
    yield self.data
    for child in self.children:
        for data in child.preorder():
            yield data
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

```python
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
```

In the above code, I don’t love the fact that I am reassigning `node` and `childiter` at every iteration of the loop.  Can you fix that so that it still works?

