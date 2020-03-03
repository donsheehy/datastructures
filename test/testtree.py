import unittest
from ds2.tree import Tree

class TestTree(unittest.TestCase):
    def testinit(self):
        Tree(['root'])
        Tree([1, [2, [3], [4]], [5, [6], [7], [8]]])

    def teststr(self):
        self.assertEqual(str(Tree([1, [2], [3]])), "1\n  2\n  3")
        self.assertEqual(str(Tree([1, [2, [3]]])), "1\n  2\n    3")

    def testcontains(self):
        T = Tree([1, [2, [3]]])
        self.assertTrue(1 in T)
        self.assertTrue(2 in T)
        self.assertTrue(3 in T)
        self.assertFalse(4 in T)

    def testeq(self):
        A = Tree([1, [2], [3]])
        B = Tree([1, [2], [3]])
        C = Tree([1, [3], [2]])
        D = Tree([1, [2, [3]]])
        E = Tree([1, [2, [3]]])
        self.assertTrue(A == B)
        self.assertTrue(D == E)
        self.assertFalse(A == C)
        self.assertFalse(B == C)
        self.assertFalse(A == D)

    def testheight(self):
        A = Tree([1, [2, [3]]])
        B = Tree([1, [2], [3], [4]])
        C = Tree([1,[1,[1,[1,[1,[1]]]]]])
        self.assertEqual(A.height(), 2)
        self.assertEqual(B.height(), 1)
        self.assertEqual(C.height(), 5)
        self.assertEqual(Tree([1]).height(), 0)

    def testpreorder(self):
        A = Tree([1, [2], [3]])
        B = Tree([1, [3], [2]])
        C = Tree([1, [2, [3]]])
        self.assertEqual(list(A.preorder()), [1, 2, 3])
        self.assertEqual(list(B.preorder()), [1, 3, 2])
        self.assertEqual(list(C.preorder()), [1, 2, 3])

    def testiter(self):
        A = Tree([4, [5], [6]])
        B = Tree([1, [3], [2]])
        C = Tree([1, [2, [3]]])
        self.assertEqual(list(A), [4, 5, 6])
        self.assertEqual(list(B), [1, 3, 2])
        self.assertEqual(list(C), [1, 2, 3])

    def testpostorder(self):
        A = Tree([1, [2], [3]])
        B = Tree([1, [3], [2]])
        C = Tree([1, [2, [3]]])
        self.assertEqual(list(A.postorder()), [2, 3, 1])
        self.assertEqual(list(B.postorder()), [3, 2, 1])
        self.assertEqual(list(C.postorder()), [3, 2, 1])

    def testlayerorder(self):
        A = Tree([1, [2], [3]])
        B = Tree([1, [2, [3]], [4]])
        C = Tree([1, [2, [3], [4]]])
        self.assertEqual(list(A.layerorder()), [1, 2, 3])
        self.assertEqual(list(B.layerorder()), [1, 2, 4, 3])
        self.assertEqual(list(C.layerorder()), [1, 2, 3, 4])


if __name__ == '__main__':
    unittest.main()
