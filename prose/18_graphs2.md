# Graph Search

Now that we have a vocabulary for dealing with graphs, we can revisit some previous topics.
For example, a tree can now be viewed as a graph with edges directed from parents to children.
Given a graph that represents a rooted tree, we could rewrite our preorder traversal using the Graph ADT.
Let's say we just want to print all the vertices.

```python
def printall(G, v):
    print(v)
    for n in G.nbrs(v):
        printall(G, n)
```

This is fine for a tree, but it quickly gets very bad as soon as there is a cycle.
In that case, there is nothing in the code to keep us from going around and around the cycle.
We can take the same approach as Hansel and Gretel: we're going to leave bread crumbs to see where we've been.
The easiest way to do this is to just keep around a set that stores the vertices that have been already visited in the search.
Thus, our `printall` method becomes the following.

```python
def printall(G, v, visited):
    print(v)
    for n in G.nbrs(v):
        if n not in visited:
            visited.add(n)
            printall(G, n)
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

```python
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

```python
def connected(G, u, v):
    return v in G.dfs(u)
```

It's possible to modify our `dfs` code to provide not only the set of connected vertices, but also the paths used in the search.
The idea is to store a dictionary that maps vertices to the previous vertex in the path from the starting vertex.
This is really encoding a tree as a dictionary that maps nodes to their parent.
The root is the starting vertex.

It differs from the trees we've seen previously in that it naturally goes up the tree from the leaves to the root rather than the reverse.
The resulting tree is called the **depth-first search tree**.
It requires only a small change to generate it.
We use the convention that the starting vertex maps to `None`.

```python
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

```python
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

```python
def bfs(self, v):
    tree = {}
    tovisit = Queue([(None, v)])
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

```python
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

## Weighted Graphs and Shortest Paths

In the **single source, all shortest paths problem**, the goal is to find the shortest path from every vertex to a given source vertex.
If the edges are assumed to have the same length, then BFS solves this problem.
However, it is common to consider **weighted graphs** in which a (positive) real number called the **weight** is assigned to each edge.
We will augment our graph ADT to support a function `wt(u,v)` that returns the weight of an edge.
Then, the weight of a path is the sum of the weights of the edges on that path.
Now, simple examples make it clear that the shortest path may not be what we get from the BFS tree.

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

```python
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
                tovisit.add((b,n), D[b] + self.wt(b,n))
    return tree, D
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

```python
def prim(self, v):
    tree = {}
    tovisit = PriorityQueue()
    tovisit.insert((None, v), 0)
    while tovisit:
        a,b = tovisit.removemin()
        if b not in tree:
            tree[b] = a
            for n in self.nbrs(b):
                tovisit.add((b,n), self.wt(b,n))
    return tree
```


## An optimization for Priority-First search

The implementation above, although correct, is not technically Dijkstra's Algorithm, but it's close.
By trying to improve its asymptotic running time, we'll get to the real Dijkstra's Algorithm.
When thinking about how to improve an algorithm, an easy first place to look is for wasted work.
In this case, we can see that many edges added to the priority queue are later removed without being used, because they lead to a vertex that has already been visited (by a shorter path).

It would be better to not have to these edges in the priority queue, but we don't know when we first see an edge whether or not a later edge will provide a short cut.
We can avoid adding a new entry to the priority and instead modify the existing entry that is no longer valid.

The idea is to store vertices rather than edges in the priority queue.
Then, we'll use the `reducepriority` method to update an entry when we find a new shorter path to a given vertex.
Although we won't know the distances at first, we'll store the shortest distance we've seen so far.
If we find a shortcut to a given vertex, we will reduce it's priority and update the priority queue.
Updating after finding a shortcut is called **edge relaxation**.
It works as follows.
The distances to the source are stored in a dictionary `D` that maps vertices to the distance, based on what we've searched so far.
If we find that `D[n] > D[u] + G.wt(u,n)`, then it would be a shorter path to `n` if we just took the shortest path from the source to `u` and appended the edge `(u,n)`.  In that case, we set `D[n] = D[u] + G.wt(u,n)` and update the priority queue.
*Note that we had this algorithm in mind when we added `reducepriority` to our Priority Queue ADT.*

Here's the code.

```python
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
                tovisit.reducepriority(n, D[n])
    return tree, D
```

An important difference with our DFS/BFS code is that the main data structure now stores vertices, not edges.
Also, we don't have to check if we've already visited a vertex, because if we have already visited it, we won't find an edge to relax (vertices are visited in order of their distance to the source).
