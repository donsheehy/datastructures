from ds2.priorityqueue import PriorityQueue

def heapsort(L):
    H = PriorityQueue(L)
    L[:] = [item for item in H]
