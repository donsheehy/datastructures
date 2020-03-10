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
