# testlistqueue.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import ListQueue

class TestListQueue(unittest.TestCase, QueueTests):
    Queue = ListQueue

if __name__ == '__main__':
    unittest.main()
