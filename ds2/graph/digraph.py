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
