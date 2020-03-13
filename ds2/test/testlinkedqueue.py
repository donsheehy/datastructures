# testlinkedqueue.py
import unittest
from ds2.test.testqueue import TestQueue
from ds2.queue import LinkedQueue

class TestListQueue(unittest.TestCase, TestQueue):
    Queue = LinkedQueue

if __name__ == '__main__':
    unittest.main()
