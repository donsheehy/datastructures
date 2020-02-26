import unittest
from ds2.sorting.mergesort_iter import BufferedIterator

class TestBufferedIterator(unittest.TestCase):
    def testinit(self):
        BufferedIterator([1,2,3])
        BufferedIterator(iter({1,5}))
        BufferedIterator({})

    def testnext(self):
        B = BufferedIterator([1,2,3])
        self.assertEqual(next(B), 1)
        self.assertEqual(next(B), 2)
        self.assertEqual(next(B), 3)
        with self.assertRaises(StopIteration):
            next(B)

    def testiter(self):
        B = BufferedIterator([3,4,5])
        myiter = iter(B)
        self.assertEqual(list(myiter), [3,4,5])

    def testpeek(self):
        B = BufferedIterator([1,2,3])
        self.assertEqual(B.peek(), 1)
        next(B)
        self.assertEqual(B.peek(), 2)
        next(B)
        self.assertEqual(B.peek(), 3)

    def testhasnext(self):
        B = BufferedIterator([5,6])
        self.assertTrue(B.hasnext())
        next(B)
        self.assertTrue(B.hasnext())
        next(B)
        self.assertFalse(B.hasnext())


if __name__ == '__main__':
    unittest.main()
