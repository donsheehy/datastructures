# testbothqueues.py
import unittest
from ds2.test.testqueue import QueueTests
from ds2.queue import ListQueue, LinkedQueue

def _test(queue_class):
    class QueueTestCase(unittest.TestCase, QueueTests):
        Queue = queue_class
    return QueueTestCase

TestLinkedQueue = _test(LinkedQueue)
TestListQueue = _test(ListQueue)
# TestYetAnotherQueue = _test(YetAnotherQueue)
# TestCrazyOtherQueue = _test(CrazyOtherQueue)

if __name__ == '__main__':
    unittest.main()
