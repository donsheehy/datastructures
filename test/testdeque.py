import unittest
from ds2.listdeque import ListDeque
from ds2.linkedlist import LinkedList
from ds2.doublylinkedlist import DoublyLinkedList

class TestDeque:
    def Deque(self):
        raise NotImplementedError

    def testaddfirst(self):
        pass
        
class TestListDeque(unittest.TestCase, TestDeque):
    Deque = ListDeque

class TestLinkedList(unittest.TestCase, TestDeque):
    Deque = LinkedList

class TestDoublyLinkedList(unittest.TestCase, TestDeque):
    Deque = DoublyLinkedList

    def testconcat(self):
        pass


if __name__ == '__main__':
    unittest.main()
