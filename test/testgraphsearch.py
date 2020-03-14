import unittest

from ds2.graph import ( EdgeSetGraph,
                        UndirectedEdgeSetGraph,
                        AdjacencySetGraph,
                        UndirectedAdjacencySetGraph,
                        Digraph,
                        Graph,
                        dfs,
                        bfs,
                        dijkstra,
                        dijkstra2,
                        prim
                        )


class TestGraphSearch(unittest.TestCase):
    Graph = Digraph

    def testdfs(self):
        G = self.Graph({1,2,3,4}, {(1,2), (2,3), (2,4)})
        dfstree = dfs(G, 1)
        self.assertEqual(dfstree[2], 1)
        self.assertEqual(dfstree[3], 2)
        self.assertEqual(dfstree[4], 2)

    def testbfs(self):
        G = self.Graph({1,2,3,4,5}, {(1,2), (2,3), (2,4), (3,5), (5,1)})
        bfstree = bfs(G, 1)
        self.assertEqual(bfstree[2], 1)
        self.assertEqual(bfstree[3], 2)
        self.assertEqual(bfstree[4], 2)
        self.assertEqual(bfstree[5], 3)

class TestWeightedSearch(unittest.TestCase):
    Graph = Digraph

    def testdijkstra(self):
        n = 10
        V = set(range(n))
        E = {(i, (i+1) % n, 1) for i in range(n)}
        G = self.Graph(V, E)
        tree, D = dijkstra(G, 3)
        self.assertEqual(D[4], 1)
        self.assertEqual(D[7], 4)

    def testprim(self):
        V = {1,2,3,4}
        E = {(i, j, i+j) for i in V for j in V}
        G = self.Graph(V, E)
        mst = prim(G)
        self.assertTrue(mst[1] == 2 or mst[2] == 1)
