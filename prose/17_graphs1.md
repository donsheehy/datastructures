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
   - `removeedge(u,v)` : Remove the edge u,v from the graph.
   - `__contains__(v)` : Return True if the vertex `v` is in the graph and return False otherwise.
   - `hasedge(u,v)` : Return True if the edge `(u,v)` is in the graph and return False otherwise.
   - `nbrs(v)` : Return an iterable collection of the (out)neighbors of `v`, i.e. those vertices `w` such that `(v, w)` is an edge.  (For directed graphs, this is the collection of out-neighbors.)
   - `__len__()` : Return the number of vertices in the graph.

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

```python {cmd id="_graph.edgesetgraph_00"}
class EdgeSetGraph:
    def __init__(self, V = (), E = ()):
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

    def removeedge(self, u, v):
        self._E.remove((u,v))

    def __contains__(self, v):
        return v in self._V

    def hasedge(self, u, v):
        return (u,v) in self._E

    def nbrs(self, v):
        return (w for u,w in self._E if u == v)

    def __len__(self):
        return len(self._V)
```

To make an undirected version of this class, we can will replace the tuples we are currently using with sets.
The problem here is that Python doesn't let us use sets as elements of sets.
Remember that mutable types like sets and lists cannot be used this way.
Thankfully, Python provides an immutable set type called `frozenset`.
It is just like a set except that it cannot be changed.
It can be used for our edge set in the undirected graph as follows.

```python {cmd id="_graph.edgesetgraph_01" continue="_graph.edgesetgraph_00"}
class UndirectedEdgeSetGraph(EdgeSetGraph):
    def addedge(self, u, v):
        self._E.add(frozenset({u,v}))

    def removeedge(self, u, v):
        self._E.remove(frozenset({u,v}))

    def nbrs(self, v):
        for u, w in self._E:
            if u == v:
                yield w
            elif w == v:
                yield u
```

## The `AdjacencySetGraph` Implementation

The major problem with previous implementation is that it's very slow to enumerate the neighbors of a vertex.
It should not be necessary to go through all the edges, just to find the ones incident to a given vertex.

An alternative approach is to store a set with each vertex and have this set contain all the neighbors of that vertex.  This allows for fast access to the neighbors.  In fact, it means that we don't have to store the edges explicitly at all.

```python {cmd id="_graph.adjacencysetgraph" hide}
from ds2.queue import ListQueue as Queue

```

```python {cmd, id="_graph.adjacencysetgraph_00" continue="_graph.adjacencysetgraph"}
class AdjacencySetGraph:
    def __init__(self, V = (), E = ()):
        self._V = set()
        self._nbrs = {}
        for v in V: self.addvertex(v)
        for e in E: self.addedge(*e)

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

    def removeedge(self, u, v):
        self._nbrs[u].remove(v)

    def __contains__(self, v):
        return v in self._nbrs

    def nbrs(self, v):
        return iter(self._nbrs[v])

    def __len__(self):
      return len(self._nbrs)
```

```python {cmd continue="_graph.adjacencysetgraph_00"}
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

```python {cmd id="_graph.adjacencysetgraph_01" continue="_graph.adjacencysetgraph_00"}
    def hasedge(self, u, v):
        return v in self._nbrs[u]
```

If `self._nbrs[u]` were a list, the method could take time linear in the degree of `u`.

To make an undirected version of the `AdjacencySetGraph`, we will let it behave like a directed graph in which every edge has a twin in the opposite direction.
This affects our `addedge` and `removeedge` methods.
It also requires us to be a little more careful about the `edges` method so as not to return twice as many edges as before.
We will use a set of frozensets as before to eliminate duplicates.

```python {cmd id="_graph.undirectedadjacencysetgraph_00"}
from ds2.graph import AdjacencySetGraph

class UndirectedAdjacencySetGraph(AdjacencySetGraph):
    def addedge(self, u, v):
        AdjacencySetGraph.addedge(self, u, v)
        AdjacencySetGraph.addedge(self, v, u)

    def removeedge(self, u, v):
        AdjacencySetGraph.removeedge(self, u, v)
        AdjacencySetGraph.removeedge(self, v, u)

    def edges(self):
        E = {frozenset(e) for e in AdjacencySetGraph.edges(self)}
        return iter(E)
```

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

```python {cmd id="_graph.adjacencysetgraph_02" continue="_graph.adjacencysetgraph_01"}
    def ispath(self, V):
      """Return True if and only if the vertices V form a path."""
      return V and all(self.hasedge(V[i-1], V[i]) for i in range(1, len(V)))

    def issimplepath(self, V):
      """Return True if and only if the vertices V form a simple path."""
      return self.ispath(V) and len(V) == len(set(V))

    def iscycle(self, V):
        """Return True if and only if the vertices V form a cycle."""
        return self.ispath(V) and V[0] == V[-1]

    def issimplecycle(self, V):
        """Return True if and only if the vertices V form a simple cycle."""
        return self.iscycle(V) and self.issimplepath(V[:-1])
```

```python {cmd continue="_graph.adjacencysetgraph_02"}
G = AdjacencySetGraph({1,2,3,4}, {(1,2),(3,1), (2,3), (3,4), (4,3)})
print("[1,2,3,1] is a path", G.ispath([1,2,3,1]))
print("[1,2,3,1] is a simple path", G.issimplepath([1,2,3,1]))
print("[1,2,3] is a simple path", G.issimplepath([1,2,3]))
print("[1,2,3] is a simple cycle:", G.issimplecycle([1,2,3]))
print("[1,2,3,1] is a simple cycle:", G.issimplecycle([1,2,3]))
print("[1,2,3,4] is a simple path:", G.issimplepath([1,2,3,4]))
print("[1,2,3,4] is a simple cycle:", G.issimplecycle([1,2,3,4]))
print("[1,2,3,4,3,1] is a cycle:", G.iscycle([1,2,3,4,3,1]))
print("[1,2,3,4,3,1] is a simple cycle:", G.issimplecycle([1,2,3,4,3,1]))
```

We say that $u$ is **connected** to $v$ if there exists a path that starts at $u$ and ends at $v$.
For an undirected graph, if $u$ is connected to $v$, then $v$ is connected to $u$.
In such graphs, we can partition the vertices into subsets called **connected components** that are all pairwise connected.  

For a directed graph, two vertices $u$ and $v$ are **strongly connected** if $u$ is connected to $v$ *and also* $v$ is connected to $u$.

Let's consider a simple method to test of two vertices are connected.
We will add it to our `AdjacencySetGraph` class.  As a first exercise, we could try to work recursively.  The idea is simple: in the base case, see if you are trying to get from a vertex to itself.  Otherwise, it suffices to check if any of the neighbors of the first vertex are connected to the last vertex.

```python {cmd continue="_graph.adjacencysetgraph_01", id="connected1"}
    def connected(self, a, b):
        if a == b: return True
        return any(self.connected(nbr, b) for nbr in self.nbrs(a))
```
Can you guess what will go wrong?
Here's an example.

```python {cmd continue="connected1" error_expected}
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

```python {cmd continue="_graph.adjacencysetgraph_01", id="connected2"}
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

# Graph Search

Now that we have a vocabulary for dealing with graphs, we can revisit some previous topics.
For example, a tree can now be viewed as a graph with edges directed from parents to children.
Given a graph that represents a rooted tree, we could rewrite our preorder traversal using the Graph ADT.
Let's say we just want to print all the vertices.

```python {cmd id="graphprintall1"}
def printall(G, v):
    print(v)
    for n in G.nbrs(v):
        printall(G, n)
```

```python {cmd continue="graphprintall1"}
from ds2.graph import AdjacencySetGraph as Graph

G = Graph({1,2,3,4}, {(1,2), (1,3), (1,4)})
printall(G, 1)
```

This is fine for a tree, but it quickly gets very bad as soon as there is a cycle.
In that case, there is nothing in the code to keep us from going around and around the cycle.
We will get a `RecursionError`.
We will take the same approach as Hansel and Gretel: we're going to leave bread crumbs to see where we've been.
The easiest way to do this is to just keep around a set that stores the vertices that have been already visited in the search.
Thus, our `printall` method becomes the following.

```python {cmd id="graphprintall2"}
def printall(G, v, visited):
    visited.add(v)
    print(v)
    for n in G.nbrs(v):
        if n not in visited:
            printall(G, n, visited)
```

```python {cmd continue="graphprintall2"}
from ds2.graph import AdjacencySetGraph as Graph

G = Graph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,1)})
printall(G, 1, set())
```


This is the most direct generalization of a recursive tree traversal into something that also traverses the vertices of a graph.
Unlike with (rooted) trees, we have to specify the starting vertex, because there is no specially marked "root" vertex in a graph.
Also, this code will not necessarily print all the vertices in a graph.
In this case, it will only print those vertices that are connected to the starting vertex.
This pattern can be made to work more generally.

## Depth-First Search

A **depth-first search** (or **DFS**) of a graph $G$ starting from a vertex $v$ will visit all the vertices connected to $v$.
It will always prioritize moving "outward" in the direction of new vertices, backtracking as little as possible.
The `printall` method above prints the vertices in a **depth-first order**.
Below is the general form of this algorithm.

```python {cmd id="graphdfs_01" continue="_graph.adjacencysetgraph_02"}
    def dfs(self, v):
        visited = {v}
        self._dfs(v, visited)
        return visited

    def _dfs(self, v, visited):
        for n in self.nbrs(v):
            if n not in visited:
                visited.add(n)
                self._dfs(n, visited)
```

With this code, it will be easy to check if two vertices are connected.
For example, one could write the following.

```python {cmd id="graphconnected_01" continue="graphdfs_01"}
def connected(G, u, v):
    return v in G.dfs(u)
```

We can try this code on a small example to see.
Notice that it is operating on a directed graph.

```python {cmd continue="graphconnected_01"}
G = AdjacencySetGraph({1,2,3,4}, {(1,2), (2,3), (3,4), (4,2)})

print("1 is connected to 4:", connected(G, 1, 4))
print("4 is connected to 3:", connected(G, 4, 3))
print("4 is connected to 1:", connected(G, 4, 1))
```

It's possible to modify our `dfs` code to provide not only the set of connected vertices, but also the paths used in the search.
The idea is to store a dictionary that maps vertices to the previous vertex in the path from the starting vertex.
This is really encoding a tree as a dictionary that maps nodes to their parent.
The root is the starting vertex.

It differs from the trees we've seen previously in that it naturally goes up the tree from the leaves to the root rather than the reverse.
The resulting tree is called the **depth-first search tree**.
It requires only a small change to generate it.
We use the convention that the starting vertex maps to `None`.

```python {cmd id="graphdfs_02" continue="_graph.adjacencysetgraph_02"}
    def dfs(self, v):
        tree = {v: None}
        self._dfs(v, tree)
        return tree

    def _dfs(self, v, tree):
        for n in self.nbrs(v):
            if n not in tree:
                tree[n] = v
                self._dfs(n, tree)
```

## Removing the Recursion

The `dfs` code above uses recursion to keep track of previous vertices, so that we can backtrack (by `return`ing) when we reach a vertex from which we can't move forward.
To remove the recursion, we replace the function call stack with our own stack.

This is not just an academic exercise.
By removing the recursion, we will reveal the structure of the algorithm in a way that will allow us to generalize it to other algorithms.
Here's the code.

```python {cmd id="_graph.adjacencysetgraph_03" continue="_graph.adjacencysetgraph_02"}
    def dfs(self, v):
        tree = {}
        tovisit = [(None, v)]
        while tovisit:
            a,b = tovisit.pop()
            if b not in tree:
                tree[b] = a
                for n in self.nbrs(b):
                    tovisit.append((b,n))
        return tree
```

## Breadth-First Search

We get another important traversal by replacing the stack with a queue.
In this case, the search prioritizes breadth over depth, resulting in a **breadth-first search** of **BFS**.

```python {cmd id="_graph.adjacencysetgraph_04" continue="_graph.adjacencysetgraph_03"}
    def bfs(self, v):
        tree = {}
        tovisit = Queue()
        tovisit.enqueue((None, v))
        while tovisit:
            a,b = tovisit.dequeue()
            if b not in tree:
                tree[b] = a
                for n in self.nbrs(b):
                    tovisit.enqueue((b,n))
        return tree
```

A wonderful property of breadth-first search is that the paths encoded in the resulting **breadth-first search tree** are the shortest paths from each vertex to the starting vertex.
Thus, BFS can be used to find the shortest path connecting pairs of vertices in a graph.

```python {cmd id="graphdistance_01" continue="_graph.adjacencysetgraph_04"}
def distance(G, u, v):
    tree = G.bfs(u)
    if v not in tree:
        return float('inf')
    edgecount = 0
    while v is not u:
        edgecount += 1
        v = tree[v]
    return edgecount
```

```python {cmd continue="graphdistance_01"}
G = AdjacencySetGraph({1,2,3,4,5}, {(1,2), (2,3), (3,4), (4,5)})
print("distance from 1 to 5:", distance(G, 1, 5))
print("distance from 2 to 5:", distance(G, 2, 5))
print("distance from 3 to 4:", distance(G, 3, 4))
```

## Weighted Graphs and Shortest Paths

In the **single source, all shortest paths problem**, the goal is to find the shortest path from every vertex to a given source vertex.
If the edges are assumed to have the same length, then BFS solves this problem.
However, it is common to consider **weighted graphs** in which a (positive) real number called the **weight** is assigned to each edge.
We will augment our graph ADT to support a function `wt(u,v)` that returns the weight of an edge.
Then, the weight of a path is the sum of the weights of the edges on that path.
Now, simple examples make it clear that the shortest path may not be what we get from the BFS tree.

```python {cmd id="_graph.digraph_00"}
from ds2.graph import AdjacencySetGraph
from ds2.priorityqueue import PriorityQueue

class Digraph(AdjacencySetGraph):
    def addedge(self, u, v, weight = 1):
        self._nbrs[u][v] = weight

    def removeedge(self, u, v):
        del self._nbrs[u][v]

    def addvertex(self, v):
        self._V.add(v)
        self._nbrs[v] = {}

    def wt(self, u, v):
        return self._nbrs[u][v]
```

```python {cmd id="_graph.graph_00"}
from ds2.graph import Digraph

class Graph(Digraph):
    def addedge(self, u, v, weight = 1):
        Digraph.addedge(self, u, v, weight)
        Digraph.addedge(self, v, u, weight)

    def removeedge(self, u, v):
        Digraph.removeedge(self, u, v)
        Digraph.removeedge(self, v, u)

    def edges(self):
        E = {frozenset(e) for e in Digraph.edges(self)}
        return iter(E)
```

One nice algorithm for the single source, all shortest paths problem on weighted graphs is called Dijkstra's algorithm.
It looks a lot like DFS and BFS except now, the stack or queue is replaced by a priority queue.
The vertices will be visited in order of their distance to the source.
These distances will be used as the priorities in the priority queue.

We'll see two different implementations.
The first, although less efficient is very close to DFS and BFS.
Recall that in those algorithms, we visit the vertices, recording the edges used in a dictionary and adding all the neighboring vertices to a stack or a queue to be traversed later.
We'll do the same here except that we'll use a priority queue to store the edges to be searched.
We'll also keep a dictionary of the distances from the start vertex that will be updated when we visit a vertex.
The priority for an edge `(u,v)` will be the distance to `u` plus the weight of `(u,v)`.
So, if we use this edge, the shortest path to `v` will go through `u`.
In this way, the tree will encode all the shortest paths from the start vertex.
Thus, the result will be not only the lengths of all the paths, but also an efficient encoding of the paths themselves.

```python {cmd id="_graph.digraph_01" continue="_graph.digraph_00"}
    def dijkstra(self, v):
        tree = {}
        D = {v: 0}
        tovisit = PriorityQueue()
        tovisit.insert((None,v), 0)
        while tovisit:
            a,b = tovisit.removemin()
            if b not in tree:
                tree[b] = a
                if a is not None:
                    D[b] = D[a] + self.wt(a,b)
                for n in self.nbrs(b):
                    tovisit.insert((b,n), D[b] + self.wt(b,n))
        return tree, D
```

Let's write a little code to see how this works.
We'll add a function to write out the path in the tree and then we'll display all the shortest paths found by the algorithm.

```python {cmd id="shortestpaths" continue="_graph.digraph_02"}
def path(tree, v):
    path = []
    while v is not None:
        path.append(str(v))
        v = tree[v]
    return ' --> '.join(path)

def shortestpaths(G, v):
    tree, D = G.dijkstra(v)
    for v in G.vertices():
        print('Vertex', v, ':', path(tree, v), ", distance = ", D[v])
```

```python {cmd continue="shortestpaths"}
G = Digraph({1,2,3}, {(1,2, 4.6), (2, 3, 9.2), (1, 3, 3.1)})
shortestpaths(G, 1)
print('------------------------')
# Adding an edge creates a shortcut to vertex 2.
G.addedge(3, 2, 1.1)
shortestpaths(G, 1)
```

## Prim's Algorithm for Minimum Spanning Trees

Recall that a subgraph of an undirected graph $G = (V,E)$ is a **spanning tree** if it is a tree with vertex set $V$.
For a weighted graph, the weight of a spanning tree is the sum of the weights of its edges.
The **Minimum Spanning Tree** (**MST**) Problem is to find *a* spanning tree of an input graph with minimum weight.
The problem comes up naturally in many contexts.

To find an algorithm for this problem, we start by trying to describe which edges should appear in the minimum spanning tree.
That is, we should think about the object we want to construct first, and only then can we think about *how* to construct it.
We employed a similar strategy when discussing sorting algorithms.
In that case, we first tried to write a function that would test for correct output.
We won't go that far now, but we will ask, "How would we know if we had the minimum spanning tree?"

One thing that would certainly be true about the minimum spanning tree is that if we removed an edge (resulting in two trees), we couldn't find a lighter weight edge connecting these two trees.
Otehrwise, that would be a spanning tree of lower weight.

Something even a little more general is true.
If we split the vertices into any two sets $A$ and $B$, the lowest weight edge with one end in $A$ and the other end in $B$ must be in the MST.
Suppose for contradiction that this edge is not in the MST.
Then, we could add that edge and form a cycle, which would have another edge spanning $A$ and $B$.
That edge could then be removed, leaving us with a lighter spanning tree.
This is a contradiction, because we assumed that we started with the MST.

So, in light of our previous graph algorithms, we can try to always add the lightest edge from the visited vertices to an unvisited vertex.
This can easily be encoded in a priority queue.

```python {cmd id="_graph.digraph_02", continue="_graph.digraph_01"}
    def prim(self):
        v = next(iter(self.vertices()))
        tree = {}
        tovisit = PriorityQueue()
        tovisit.insert((None, v), 0)
        while tovisit:
            a,b = tovisit.removemin()
            if b not in tree:
                tree[b] = a
                for n in self.nbrs(b):
                    tovisit.insert((b,n), self.wt(b,n))
        return tree
```

The following example clearly shows that the minimum spanning tree and the shortest path tree are not the same.

```python {cmd id="msts" continue="_graph.graph_00"}
G = Graph({1,2,3,4,5}, {(1, 2, 1),
                        (2, 3, 1),
                        (1, 3, 2),
                        (3, 4, 1),
                        (3, 5, 3),
                        (4, 5, 2),
                       })
mst = G.prim()
sp, D = G.dijkstra(1)
print(mst)
print(sp)
```
## An optimization for Priority-First search

The implementation above, although correct, is not technically Dijkstra's Algorithm, but it's close.
By trying to improve its asymptotic running time, we'll get to the real Dijkstra's Algorithm.
When thinking about how to improve an algorithm, an easy first place to look is for wasted work.
In this case, we can see that many edges added to the priority queue are later removed without being used, because they lead to a vertex that has already been visited (by a shorter path).

It would be better to not have to these edges in the priority queue, but we don't know when we first see an edge whether or not a later edge will provide a short cut.
We can avoid adding a new entry to the priority and instead modify the existing entry that is no longer valid.

The idea is to store vertices rather than edges in the priority queue.
Then, we'll use the `changepriority` method to update an entry when we find a new shorter path to a given vertex.
Although we won't know the distances at first, we'll store the shortest distance we've seen so far.
If we find a shortcut to a given vertex, we will reduce it's priority and update the priority queue.
Updating after finding a shortcut is called **edge relaxation**.
It works as follows.
The distances to the source are stored in a dictionary `D` that maps vertices to the distance, based on what we've searched so far.
If we find that `D[n] > D[u] + G.wt(u,n)`, then it would be a shorter path to `n` if we just took the shortest path from the source to `u` and appended the edge `(u,n)`.  In that case, we set `D[n] = D[u] + G.wt(u,n)` and update the priority queue.
*Note that we had this algorithm in mind when we added `changepriority` to our Priority Queue ADT.*

Here's the code.

```python {cmd id="dijkstra2" continue="_graph.digraph_02"}
    def dijkstra2(self, v):
        tree = {v: None}
        D = {u: float('inf') for u in self.vertices()}
        D[v] = 0
        tovisit = PriorityQueue([(u, D[u]) for u in self.vertices()])
        while tovisit:
            u = tovisit.removemin()
            for n in self.nbrs(u):
                if D[u] + self.wt(u,n) < D[n]:
                    D[n] = D[u] + self.wt(u,n)
                    tree[n] = u
                    tovisit.changepriority(n, D[n])
        return tree, D
```

```python {cmd continue="dijkstra2"}
V = {1,2,3,4,5}
E = {(1,2,1),
     (2,3,2),
     (1,3,2),
     (3,4,2),
     (2,5,2)
    }
G = Digraph(V, E)
tree, D = G.dijkstra2(1)
print(tree, D)
```

An important difference with our DFS/BFS code is that the main data structure now stores vertices, not edges.
Also, we don't have to check if we've already visited a vertex, because if we have already visited it, we won't find an edge to relax (vertices are visited in order of their distance to the source).
