# testlinkedqueue.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import LinkedQueue

class TestLinkedQueue(unittest.TestCase, QueueTests):
    Queue = LinkedQueue

if __name__ == '__main__':
    unittest.main()
