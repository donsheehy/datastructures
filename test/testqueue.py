import unittest
from ds2.listqueue import ListQueue
from ds2.linkedqueue import LinkedQueue

class _:
    class TestQueue(unittest.TestCase()):
        def testinit(self):
            Q = self.Queue()

class TestListQueue(_.TestQueue):
    Queue = ListQueue


class TestLinkedQueue(_.TestQueue):
    Queue = ListQueue


if __name__ == '__main__':
    unittest.main()
