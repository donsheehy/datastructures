# linkedqueue.py
from linkedlist import LinkedList

class LinkedQueue:
    def __init__(self):
        self._L = LinkedList()

    def enqueue(self, item):
        self._L.addlast(item)

    def dequeue(self):
        return self._L.removefirst()

    def __len__(self):
        return len(self._L)

