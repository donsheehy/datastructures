from ds2.queue import ListQueue as Queue
from ds2.priorityqueue import PriorityQueue
from ds2.graph import Graph


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

def bfs(G, v):
    tree = {}
    tovisit = Queue()
    tovisit.enqueue((None, v))
    while tovisit:
        a,b = tovisit.dequeue()
        if b not in tree:
            tree[b] = a
            for n in G.nbrs(b):
                tovisit.enqueue((b,n))
    return tree

def distance(G, u, v):
    tree = G.bfs(u)
    if v not in tree:
        return float('inf')
    edgecount = 0
    while v is not u:
        edgecount += 1
        v = tree[v]
    return edgecount

def dijkstra(G, v):
    tree = {}
    D = {v: 0}
    tovisit = PriorityQueue()
    tovisit.insert((None,v), 0)
    for a,b in tovisit:
        if b not in tree:
            tree[b] = a
            if a is not None:
                D[b] = D[a] + G.wt(a,b)
            for n in G.nbrs(b):
                tovisit.insert((b,n), D[b] + G.wt(b,n))
    return tree, D

def prim(G):
    v = next(iter(G.vertices()))
    tree = {}
    tovisit = PriorityQueue()
    tovisit.insert((None, v), 0)
    for a, b in tovisit:
        if b not in tree:
            tree[b] = a
            for n in G.nbrs(b):
                tovisit.insert((b,n), G.wt(b,n))
    return tree

def dijkstra2(G, v):
    tree = {v: None}
    D = {u: float('inf') for u in G.vertices()}
    D[v] = 0
    tovisit = PriorityQueue(entries = [(u, D[u]) for u in G.vertices()])
    for u in tovisit:        
        for n in G.nbrs(u):
            if D[u] + G.wt(u,n) < D[n]:
                D[n] = D[u] + G.wt(u,n)
                tree[n] = u
                tovisit.changepriority(n, D[n])
    return tree, D
