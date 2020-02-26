import unittest
from ds2.select import quickselect, quickselect_recursive

class SelectTests:
    def testselect(self):
        A = [3,5,7,9,4,6,8]
        self.assertEqual(self.select(A, 1), 3)
        self.assertEqual(self.select(A, 2), 4)
        self.assertEqual(self.select(A, 3), 5)
        self.assertEqual(self.select(A, 4), 6)
        self.assertEqual(self.select(A, 5), 7)
        self.assertEqual(self.select(A, 6), 8)

    def testmanyruns(self):
        A = list(range(100))
        self.assertEqual(self.select(A,1), 0)
        self.assertEqual(self.select(A,1), 0)
        for i in range(100):
            self.assertEqual(self.select(A,i+1), i)

    def testonstrings(self):
        A = ['abc', 'def', 'aa', 'b']
        self.assertEqual(self.select(A, 4), 'def')
        self.assertEqual(self.select(A, 3), 'b')
        self.assertEqual(self.select(A, 2), 'abc')
        self.assertEqual(self.select(A, 1), 'aa')

    def testbigexample(self):
        A = [1] * 1000 + [2] + [3] * 1000
        self.assertEqual(self.select(A, 1001), 2)

def _test(selectalgorithm):
    """Return a new testcase class for the given sorting algorithm.
    """
    class MySelectTests(unittest.TestCase, SelectTests):
        def select(self, L, index):
            return selectalgorithm(L, index)
    return MySelectTests

TestQuickSelect = _test(quickselect)
TestQuickSelectRecursive = _test(quickselect_recursive)

if __name__ == '__main__':
    unittest.main()
