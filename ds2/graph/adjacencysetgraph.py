from ds2.queue import ListQueue as Queue


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

    def hasedge(self, u, v):
        return v in self._nbrs[u]

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
