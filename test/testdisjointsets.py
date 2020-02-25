import unittest
from ds2.disjointsets import (  DisjointSetsMapping,
                                DisjointSetsLabels,
                                DisjointSetsForest,
                                DisjointSetsPathCompression,
                                DisjointSetsTwoPassPC,
                                DisjointSetsMergeByHeight,
                                DisjointSetsMergeByWeight,
                                DisjointSets
                                )

class DisjointSetsTests:
    def testunionfind(self):
        ds = self.DisjointSets([1,2,3,4,5,6])
        ds.union(1,2)
        ds.union(1,5)
        ds.union(3,4)

        self.assertTrue(ds.find(2,5) is True)
        self.assertTrue(ds.find(1,5) is True)
        self.assertTrue(ds.find(2,1) is True)
        self.assertTrue(ds.find(5,1) is True)
        self.assertTrue(ds.find(1,1) is True)
        self.assertTrue(ds.find(6,6) is True)
        self.assertTrue(ds.find(1,3) is False)
        self.assertTrue(ds.find(2,4) is False)
        self.assertTrue(ds.find(2,6) is False)

def _test(implementation):
    class MyTestDisjointSets(unittest.TestCase, DisjointSetsTests):
        DisjointSets = implementation
    return MyTestDisjointSets

TestDisjointSetsMapping = _test(DisjointSetsMapping)
TestDisjointSetsLabels = _test(DisjointSetsLabels)
TestDisjointSetsForest = _test(DisjointSetsForest)
TestDisjointSetsPathCompression = _test(DisjointSetsPathCompression)
TestDisjointSetsTwoPassPC = _test(DisjointSetsTwoPassPC)
TestDisjointSetsMergeByHeight = _test(DisjointSetsMergeByHeight)
TestDisjointSetsMergeByWeight = _test(DisjointSetsMergeByWeight)
TestDisjointSets = _test(DisjointSets)

if __name__ == '__main__':
    unittest.main()
