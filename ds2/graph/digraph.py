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

