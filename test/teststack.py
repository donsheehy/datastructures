import unittest
from ds2.liststack import ListStack
from ds2.badstack import BadStack

class TestStack:
    def Stack(self):
        raise NotImplementedError

    def testinit(self):
        s = self.Stack()

    def testpushandpop(self):
        s = self.Stack()
        s.push(3)
        s.push(5)
        self.assertEqual(s.pop(), 5)
        s.push(7)
        self.assertEqual(s.pop(), 7)
        self.assertEqual(s.pop(), 3)

    def testpeek(self):
        s = self.Stack()
        s.push("first")
        s.push("second")
        s.push("third")
        self.assertEqual(s.peek(), "third")
        self.assertEqual(s.peek(), "third")
        s.pop()
        self.assertEqual(s.peek(), "second")
        self.assertEqual(s.peek(), "second")
        s.pop()
        self.assertEqual(s.peek(), "first")

    def testlen(self):
        s = self.Stack()
        self.assertEqual(len(s), 0)
        for i in range(10):
            s.push(i)
            s.push(i+1)
            self.assertEqual(len(s), i+2)
            s.pop()
            self.assertEqual(len(s), i+1)

    def testisempty(self):
        s = self.Stack()
        self.assertTrue(s.isempty())
        s.push(1)
        self.assertFalse(s.isempty())
        s.pop()
        self.assertTrue(s.isempty())

class TestListStack(unittest.TestCase, TestStack):
    Stack = ListStack

class TestBadStack(unittest.TestCase, TestStack):
    Stack = BadStack

if __name__ == '__main__':
    unittest.main()
