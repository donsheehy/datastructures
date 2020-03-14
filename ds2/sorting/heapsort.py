from ds2.priorityqueue import PriorityQueue

def heapsort(L):
    H = PriorityQueue(L)
    L[:] = [item for item in H]

def heapsorted(L):
    H = PriorityQueue(L)
    return [item for item in H]
