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

