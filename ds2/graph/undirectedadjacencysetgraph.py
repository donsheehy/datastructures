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
