import unittest
from ds2.deque import ListDeque, LinkedList, DoublyLinkedList

class DequeTests:
    def Deque(self):
        raise NotImplementedError

    def testaddfirst(self):
        D = self.Deque()
        D.addfirst(4)
        D.addfirst(2)

    def testremovefirst(self):
        D = self.Deque()
        D.addfirst(4)
        D.addfirst(3)
        self.assertEqual(D.removefirst(), 3)

    def testaddlast(self):
        D = self.Deque()
        D.addlast(3)
        D.addfirst(1)
        D.addlast(2)
        D.addfirst(0)
        self.assertEqual(D.removefirst(), 0)
        self.assertEqual(D.removefirst(), 1)
        self.assertEqual(D.removefirst(), 3)
        self.assertEqual(D.removefirst(), 2)

    def testremovelast(self):
        D = self.Deque()
        for i in range(6,10):
            D.addlast(i)
        self.assertEqual(D.removelast(), 9)
        self.assertEqual(len(D), 3)
        D.removefirst() # remove the 6 from the front.
        self.assertEqual(D.removelast(), 8)
        self.assertEqual(D.removelast(), 7)
        self.assertEqual(len(D), 0)


class TestListDeque(unittest.TestCase, DequeTests):
    Deque = ListDeque

class TestLinkedList(unittest.TestCase, DequeTests):
    Deque = LinkedList

class TestDoublyLinkedList(unittest.TestCase, DequeTests):
    Deque = DoublyLinkedList

    def testconcatenation(self):
        A = self.Deque()
        B = self.Deque()
        for i in range(9):
            A.addlast(i)
            B.addlast(i+9)
        A += B
        self.assertEqual(len(A), 18)
        self.assertEqual(len(B), 0)
        for i in range(18):
            self.assertEqual(A.removefirst(), i)

    def testconcattoempty(self):
        A = self.Deque()
        C = self.Deque()
        A.addlast(1)
        A.addlast(2)
        C += A
        self.assertEqual(len(C), 2)
        self.assertEqual(C.removefirst(), 1)
        self.assertEqual(C.removefirst(), 2)

    def testconcatempty(self):
        A = self.Deque()
        C = self.Deque()
        C += A
        self.assertEqual(len(C), 0)



if __name__ == '__main__':
    unittest.main()
