from ds2.disjointsets import DisjointSets

def kruskall(G):
    V = list(G.vertices())
    UF = DisjointSets(V)
    edges = sorted(G.edges(), key = lambda e :G.wt(*e))
    T = Graph(V, set())
    for u, v in edges:
        if not UF.find(u, v):
            UF.union(u, v)
            T.addedge(u, v)
    return T
