import unittest
from ds2.orderedlist import OrderedList, OrderedListSimple

class OrderedListTests:
    def OrderedList(self):
        raise NotImplementedError

    def testadd(self):
        L = self.OrderedList()
        for i in [3,1,4,0,2]:
            L.add(i)

    def testcontains(self):
        L = self.OrderedList()
        for i in [3,1,4,0,2]:
            L.add(i)
        L.__contains__(2)
        self.assertTrue(0 in L)
        self.assertTrue(4 in L)

    def testgeitem(self):
        L = self.OrderedList()
        for i in [3,1,100,2,4]:
            L.add(i)
        self.assertEqual(L[0], 1)
        self.assertEqual(L[1], 2)
        self.assertEqual(L[2], 3)
        self.assertEqual(L[3], 4)
        self.assertEqual(L[4], 100)

    def testremove(self):
        L = self.OrderedList()
        for i in [3,1,100,2,4]:
            L.add(i)
        self.assertEqual(L[1], 2)
        self.assertEqual(len(L), 5)
        L.remove(2)
        self.assertEqual(L[1], 3)
        self.assertEqual(len(L), 4)
        L.remove(100)
        self.assertEqual(len(L), 3)

    def testiter(self):
        L = self.OrderedList()
        for i in [3,1,4,0,2]:
            L.add(i)
        self.assertEqual(list(L), [0,1,2,3,4])

    def testlen(self):
        L = self.OrderedList()
        self.assertEqual(len(L), 0)
        for i in [3,1,4,0,2]:
            L.add(i)
        self.assertEqual(len(L), 5)

class TestOrderedList(unittest.TestCase, OrderedListTests):
    OrderedList = OrderedList

class TestOrderedListSimple(unittest.TestCase, OrderedListTests):
    OrderedList = OrderedListSimple


if __name__ == '__main__':
    unittest.main()
