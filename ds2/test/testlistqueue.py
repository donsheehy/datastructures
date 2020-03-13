# testlistqueue.py
import unittest
from ds2.test.testqueue import TestQueue
from ds2.queue import ListQueue

class TestListQueue(unittest.TestCase, TestQueue):
    Queue = ListQueue

if __name__ == '__main__':
    unittest.main()
