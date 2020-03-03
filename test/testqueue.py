import unittest
from ds2.queue import ListQueueSimple, ListQueue, ListQueueFakeDelete
from ds2.queue import LinkedQueue


class QueueTests:
    def Queue():
        raise NotImplementedError

    def testaddandremoveoneitem(self):
        q = self.Queue()
        q.enqueue(3)
        self.assertEqual(q.dequeue(), 3)

    def testalternatingaddremove(self):
        q = self.Queue()
        for i in range(1000):
            q.enqueue(i)
            self.assertEqual(q.dequeue(), i)

    def testpeek(self):
        q = self.Queue()
        q.enqueue(12)
        q.enqueue(20)
        self.assertEqual(q.peek(), 12)
        self.assertEqual(q.peek(), 12)
        q.dequeue()
        self.assertEqual(q.peek(), 20)

    def testmanyoperations(self):
        q = self.Queue()
        for i in range(1000):
            q.enqueue(2 * i + 3)
        for i in range(1000):
            self.assertEqual(q.dequeue(), 2 * i + 3)

    def testlength(self):
        q = self.Queue()
        self.assertEqual(len(q), 0)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 10)
        for i in range(10):
            q.enqueue(i)
        self.assertEqual(len(q), 20)
        for i in range(15):
            q.dequeue()
        self.assertEqual(len(q), 5)

    def testisempty(self):
        Q = self.Queue()
        self.assertTrue(Q.isempty())
        Q.enqueue(100)
        self.assertFalse(Q.isempty())
        Q.dequeue()
        self.assertTrue(Q.isempty())


class TestListQueueSimple(unittest.TestCase, QueueTests):
    Queue = ListQueueSimple

class TestListQueueFakeDelete(unittest.TestCase, QueueTests):
    Queue = ListQueueFakeDelete

class TestListQueue(unittest.TestCase, QueueTests):
    Queue = ListQueue

class TestLinkedQueue(unittest.TestCase, QueueTests):
    Queue = LinkedQueue


if __name__ == '__main__':
    unittest.main()
