import unittest

from ds2.graph import ( EdgeSetGraph,
                        UndirectedEdgeSetGraph,
                        AdjacencySetGraph
                        )

class GeneralGraphTests:
    def testinit(self):
        G = self.Graph({},{})

class DigraphTests(GeneralGraphTests):
    pass

class GraphTests(GeneralGraphTests):
    pass

class TestEdgeSetGraph(unittest.TestCase, DigraphTests):
    Graph = EdgeSetGraph

class TestUndirectedEdgeSetGraph(unittest.TestCase, GraphTests):
    Graph = UndirectedEdgeSetGraph

class TestAdjacencySetGraph(unittest.TestCase, DigraphTests):
    Graph = AdjacencySetGraph

class TestAdjacencySetGraph(unittest.TestCase, DigraphTests):
    Graph = AdjacencySetGraph


if __name__ == '__main__':
    unittest.main()
