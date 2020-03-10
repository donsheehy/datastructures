def issorted(L):
    for i in range(len(L)-1):
        if L[i]>L[i+1]:
            return False
    return True

def dumbersort(L):
    for i in range(len(L)-1):
        if L[i]>L[i+1]:
            L[i], L[i+1] = L[i+1], L[i]

def dumbsort(L):
    while (not issorted(L)):
        dumbersort(L)
