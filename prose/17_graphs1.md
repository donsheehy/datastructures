# Graphs

The **graph** is a fundamental mathematical object in computer science.  Graphs are used to abstract networks, maps, program control flow, probabilistic models, and even data structures among many other computer science concepts.

A good mental model to start with is a road map of a country.  There are cities and roads connecting those cities.  Graphs are ideal for describing such situations where there are items and connections between them.

Formally, a graph is a pair $(V, E)$ where $V$ is any set and $E$ is a set of pairs of elements of $V$.  We call $V$ the **vertex set** and $E$ the **edge set**.  Just using the definition of a graph and the standard python collections, we could store a graph as follows.

```python
G = ({1,2,3,4}, {(1,2), (1,3), (1,4)})
```
The graph `G` has 4 vertices and 3 edges.  Such a graph is often depicted 4 labeled circles for vertices and lines between them depicting the edges.  Because tuples are ordered, we would add arrowheads.  This indicates a **directed graph** or **digraph**.  If the ordering of the vertices in an edge does not matter, we have an **undirected graph**.  There will be no major difference between an undirected graph and a digraph that has a matched pair $(v,u)$ for every $(u,v)$ in $E$.

Usually, we will disallow **self-loops**, edges that start and end at the same vertex, and **multiple edges** between the same pair of vertices.  Graphs without self-loops and multiple edges are called **simple graphs**.

If two vertices are connected by an edge, we say they are **adjacent**.
We all call such vertices **neighbors**.
For an edge $e = (u,v)$, we say that the vertices $u$ and $v$ are **incident** to the edge $e$.  The **degree of a vertex** is the number of neighbors it has.  For digraphs, we distinguish between **in-degree** and **out-degree**, the number of in-neighbors and out-neighbors respectively.

## A Graph ADT

First, let's establish the minimal ADT for a simple, directed graph.
We should be able to use any (hashable) type for the vertices.
We want to be able to create the graph from a collection of vertices and a collection of ordered pairs of vertices.

   - `__init__(V, E)` : Initialize a new graph with vertex set `V` and edge set `E`.
   - `vertices()` : Return an iterable collection of the vertices.
   - `edges()` : Return an iterable collection of the edges.
   - `addvertex(v)` : Add a new vertex to the graph.  The new vertex is identified with the `v` object.
   - `addedge(u, v)` : Add a new edge to the graph between the vertices with keys `u` and `v`.
   - `nbrs(v)` : Return an iterable collection of the (out)neighbors of `v`, i.e. those vertices `w` such that `(v, w)` is an edge.  (For directed graphs, this is the collection of out-neighbors.)

There are several error conditions to consider. For example, what happens if a vertex is added more than once?
What happens if an edge `(u,v)` is added, but `u` is not a vertex in the graph?
What if one calls `nbrs(v)` and `v` is not a vertex in the graph?
We will deal with these later.
For now, let's get something working.

## The `EdgeSetGraph` Implementation

Cleverness comes second.
First, let's write a Graph class that is as close as possible to the mathematical definition of a graph.
It will store a set for the vertices and a set of pairs (2-tuples) for the edges.
To get the neighbors of a vertex, it will iterate over all edges in the graph.

```python
class EdgeSetGraph:
    def __init__(self, V, E):
        self._V = set()
        self._E = set()
        for v in V: self.addvertex(v)
        for u,v in E: self.addedge(u,v)

    def vertices(self):
        return iter(self._V)

    def edges(self):
        return iter(self._E)

    def addvertex(self, v):
        self._V.add(v)

    def addedge(self, u, v):
        self._E.add((u,v))

    def nbrs(self, v):
        return (w for u,w in self._E if u == v)
```

To make an undirected version of this class, we can simply modify the `addedge` method to add an edge in each direction.
We also change the `nbrs` method to work with unordered pairs (sets).

```python
class UndirectedEdgeSetGraph(EdgeSetGraph):
    def addedge(self, u, v):
        self._E.add((u,v))
        self._E.add((v,u))

    def edges(self):
        edgeset = set()
        for u,v in self._E:
            if (v,u) not in edgeset:
                edgeset.add((u,v))
        return iter(edgeset)
```

## The `AdjacencySetGraph` Implementation

The major problem with previous implementation is that it's very slow to enumerate the neighbors of a vertex.
It should not be necessary to go through all the edges, just to find the ones incident to a given vertex.

An alternative approach is to store a set with each vertex and have this set contain all the neighbors of that vertex.  This allows for fast access to the neighbors.  In fact, it means that we don't have to store the edges explicitly at all.

```python {cmd, id='adjacencysetgraph'}
class AdjacencySetGraph:
    def __init__(self, V, E):
        self._V = set()
        self._nbrs = {}
        for v in V: self.addvertex(v)
        for u,v in E: self.addedge(u,v)

    def vertices(self):
        return iter(self._V)

    def edges(self):
        for u in self._V:
            for v in self.nbrs(u):
                yield (u,v)

    def addvertex(self, v):
        self._V.add(v)
        self._nbrs[v] = set()

    def addedge(self, u, v):
        self._nbrs[u].add(v)

    def nbrs(self, v):
        return iter(self._nbrs[v])
```

```python {cmd continue="adjacencysetgraph"}
G = AdjacencySetGraph({1,2,3}, {(1,2),(2,1),(1,3)})
print("neighbors of 1:", list(G.nbrs(1)))
print("neighbors of 2:", list(G.nbrs(2)))
print("neighbors of 3:", list(G.nbrs(3)))
```

Let's do a very simple example to make sure it works as we expect it to.

One design decision that may seem rather strange is that we do not have a class for vertices or edges.
As of now, we are exploiting the **polymorphism** of python, which allows us to use any (hashable) type for the vertex set.
Recall that polymorphism (in this context) is the ability to call the same function on different types of objects.
This can be very convenient as it allows one to put a graph structure on top of any set.

As written, there is no clear reason to use a set for the neighbors rather than a list.
One case where the set is better is if we want to test if the graph contains a particular edge.  With the `AdjacencySetGraph` above, this method could be implemented as follows.

```python
    def hasedge(self, u, v):
        return v in self._nbrs[u]
```

If `self._nbrs[u]` were a list, the method could take time linear in the degree of `u`.

## Paths and Connectivity

A **path** in a graph $G = (V,E)$ is a sequence of vertices connected by edges.
That is, a nonempty sequence of vertices $(v_0, v_1,\ldots, v_k)$ is a path from $v_0$ to $v_k$ as long as $(v_{i-1}, v_i)\in E$ for all $i \in \{1,\ldots, k\}$.
We say a **path is simple** if it does not repeat any vertices.
The **length of a path** is the number of edges.
A single vertex can be seen as a path of length zero.

A **cycle** is a path of length at least one that starts and ends at the same vertex.
The **length of a cycle** is the number of edges.
A **cycle is simple** if is is a cycle and removing the last edge results in a simple path, i.e., there are no repeated vertices until the last one.

To solidify these definitions, we could write a couple methods to check them.

```python
def ispath(G, V):
  """Return True if and only if the vertices V form a path in G."""
  return V and all(G.hasedge(V[i-1], V[i]) for i in range(1, len(V)))

def issimplepath(G, V):
  """Return True if and only if the vertices V form a simple path in G."""
  return ispath(G, V) and len(V) == len(set(V))

def iscycle(G, V):
    """Return True if and only if the vertices V form a cycle in G."""
    return ispath(G, V) and V[0] == V[-1]

def issimplecycle(G, V):
    """Return True if and only if the vertices V form a simple cycle in G."""
    return iscycle(G,V) and issimplepath(G, V[:-1])
```

We say that $u$ is **connected** to $v$ if there exists a path that starts at $u$ and ends at $v$.
For an undirected graph, if $u$ is connected to $v$, then $v$ is connected to $u$.
In such graphs, we can partition the vertices into subsets called **connected components** that are all pairwise connected.  

For a directed graph, two vertices $u$ and $v$ are **strongly connected** if $u$ is connected to $v$ *and also* $v$ is connected to $u$.

Let's consider a simple method to test of two vertices are connected.
We will add it to our `AdjacencySetGraph` class.  As a first exercise, we could try to work recursively.  The idea is simple: in the base case, see if you are trying to get from a vertex to itself.  Otherwise, it suffices to check if any of the neighbors of the first vertex are connected to the last vertex.

```python {cmd continue="adjacencysetgraph", id="connected1"}
    def connected(self, a, b):
        if a == b: return True
        return any(self.connected(nbr, b) for nbr in self.nbrs(a))
```
Can you guess what will go wrong?
Here's an example.

```python {cmd continue='connected1'}
G = AdjacencySetGraph({1,2,3}, {(1,2), (2,3)})
assert(G.connected(1,2))
assert(G.connected(1,3))
assert(not G.connected(3,1))
print("First graph is okay.")

H = AdjacencySetGraph({1,2,3}, {(1,2), (2,1), (2,3)})
try:
    H.connected(1,3)
except RecursionError:
    print("There was too much recursion!")
```

It's clear that if the graph has any cycles, we can't check connectivity this way.  To deal with cycles, we can keep a set of visited vertices.  Recall that this is called memoization.

```python {cmd continue="adjacencysetgraph", id="connected2"}
    def connected(self, a, b):
        return self._connected(a, b, set())

    def _connected(self, a, b, visited):
        if a in visited: return False
        if a == b: return True
        visited.add(a)
        return any(self._connected(nbr, b, visited) for nbr in self.nbrs(a))
```

Now, we can try again and see what happens.

```python {cmd continue='connected2'}
H = AdjacencySetGraph({1,2,3}, {(1,2), (2,1), (2,3)})
try:
    assert(H.connected(1,2))
    assert(H.connected(1,3))
except RecursionError:
    print('There was too much recursion!')
print('It works now!')
```
