import unittest
from ds2.tree import Tree

class TestTree(unittest.TestCase):
    def testinit(self):
        Tree(['root'])

    def teststr(self):
        pass

    def testcontains(self):
        T = Tree([1, [2, [3]]])

    def testeq(self):
        pass

    def testheight(self):
        pass

    def testpreorder(self):
        pass

    def testiter(self):
        pass

    def testpostorder(self):
        pass

    def testlayerorder(self):
        pass

if __name__ == '__main__':
    import generatecode
    unittest.main()
