import unittest
from ds2.orderedmapping import (BSTMapping,
                                BalancedBST,
                                WBTree,
                                AVLTree,
                                SplayTree
                                )

class OrderedMappingTests:
    """ This Testcase only covers those aspects of an ordered mapping that go
    beyond the Mapping ADT.

    It is assumed that classes implementing the Mapping ADT should have those
    methods tested in `testmapping.py`.
    """
    def testfloor(self):
        M = self.OrderedMapping()
        keys = [4,2,1,3,5,0,7,6]
        for i in keys:
            M[i] = i + 1
        self.assertEqual(M.floor(2), (2, 3))
        self.assertEqual(M.floor(2.0), (2, 3))
        self.assertEqual(M.floor(2.1), (2, 3))
        self.assertEqual(M.floor(3.5), (3, 4))
        self.assertEqual(M.floor(7.5), (7, 8))
        self.assertEqual(M.floor(75), (7, 8))
        self.assertEqual(M.floor(-1), (None, None))

    def testflooronempty(self):
        M = self.OrderedMapping()
        self.assertEqual(M.floor(0), (None, None))

    def testremove(self):
        M = self.OrderedMapping()
        M[3] = 3
        M[1] = 1
        M[5] = 5
        self.assertEqual(M.floor(4), (3,3))
        M.remove(3)
        self.assertEqual(M.floor(4), (1,1))

    def testiter(self):
        M = self.OrderedMapping()
        for i in [9,1,2,6,3,4]:
            M[i] = None
        self.assertEqual(list(M), [1,2,3,4,6,9])

def _test(orderedmapping):
    """ Produce a TestCase class that uses the given implementation.
    """
    class OrderedMappingTestCase(unittest.TestCase, OrderedMappingTests):
        OrderedMapping = orderedmapping
    return OrderedMappingTestCase

TestBSTMapping = _test(BSTMapping)
TestBalancedBST = _test(BalancedBST)
TestWBTree = _test(WBTree)
TestAVLTree = _test(AVLTree)
TestSplayTree = _test(SplayTree)

if __name__ == '__main__':
    unittest.main()
