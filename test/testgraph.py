import unittest

from ds2.graph import ( EdgeSetGraph,
                        UndirectedEdgeSetGraph,
                        AdjacencySetGraph,
                        UndirectedAdjacencySetGraph,
                        Digraph,
                        Graph,
                        )

class GeneralGraphTests:
    def testinit(self):
        G = self.Graph({},{})
        G = self.Graph({1,2,3}, {(1,2),(2,3)})

    def testinit_empty(self):
        G = self.Graph()

    def testinit_no_edges(self):
        G = self.Graph([1,2,3], ())

    def testlen(self):
        G = self.Graph({1,2,3}, {(1,2)})
        self.assertEqual(len(G), 3)
        G.addvertex(3)
        self.assertEqual(len(G), 3)
        G.addvertex(4)
        self.assertEqual(len(G), 4)
        G.addedge(2,3)
        self.assertEqual(len(G), 4)

    def testcontains(self):
        G = self.Graph([1,2,3,4], [(2,4), (1,3)])
        for v in [1,2,3,4]:
            self.assertTrue(v in G)
        self.assertTrue(0 not in G)
        self.assertTrue('2' not in G)


class DigraphTests(GeneralGraphTests):
    def testhasedge(self):
        G = self.Graph([1,2,3], [[1,2], [3,1]])
        self.assertTrue(G.hasedge(1,2))
        self.assertFalse(G.hasedge(2,1))
        self.assertTrue(G.hasedge(3,1))
        self.assertFalse(G.hasedge(1,3))

    def testremoveedge(self):
        G = self.Graph([1,2,3], [(1,2), (1,3), (2,1)])
        G.removeedge(1,2)
        self.assertTrue(G.hasedge(2,1))
        self.assertTrue(G.hasedge(1,3))
        self.assertFalse(G.hasedge(1,2))

    def testremoveedge_not_an_edge(self):
        G = self.Graph([1,2,3], [(1,2), (1,3), (2,1)])
        with self.assertRaises(KeyError):
            G.removeedge(3,1)

    def testvertices(self):
        G = self.Graph()
        G.addvertex('a')
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('b')
        self.assertEqual(set(G.vertices()), {'a', 'b'})
        G.addvertex('c')
        self.assertEqual(set(G.vertices()), {'a', 'b', 'c'})

    def testedges(self):
        G = self.Graph([2,4,6], [(2,4), (4,6)])
        E = set(G.edges())
        self.assertEqual(len(E), 2)
        self.assertTrue((2,6) not in E and (6,2) not in E)
        G.addedge(2,6)
        E = set(G.edges())
        self.assertEqual(len(E), 3)
        self.assertTrue((2,4) in E)


class GraphTests(GeneralGraphTests):
    def testremoveedge_removesbothdirections(self):
        G = self.Graph({'a', 'b', 'c'}, {('a', 'b'), ('b','c')})
        G.removeedge('a', 'b')
        self.assertFalse(G.hasedge('b', 'a'))

    def testnbrs(self):
        G = self.Graph([2,4,6], [(2,4), (4,6)])
        self.assertEqual(set(G.nbrs(2)), {4})
        self.assertEqual(set(G.nbrs(4)), {2,6})
        self.assertEqual(set(G.nbrs(6)), {4})

    def testedges(self):
        G = self.Graph([2,4,6], [(2,4), (4,6)])
        E = list(G.edges())
        self.assertEqual(len(E), 2)

class TestEdgeSetGraph(unittest.TestCase, DigraphTests):
    Graph = EdgeSetGraph

class TestUndirectedEdgeSetGraph(unittest.TestCase, GraphTests):
    Graph = UndirectedEdgeSetGraph

class TestUndirectedAdjacencySetGraph(unittest.TestCase, GraphTests):
    Graph = UndirectedAdjacencySetGraph

class TestDigraph(unittest.TestCase, DigraphTests):
    Graph = Digraph

class TestGraph(unittest.TestCase, GraphTests):
    Graph = Graph


if __name__ == '__main__':
    unittest.main()
