def mergesort(L):
    # Base Case!
    if len(L) < 2:
        return

    # Divide!
    mid = len(L) // 2
    A = L[:mid]
    B = L[mid:]

    # Conquer!
    mergesort(A)
    mergesort(B)

    # Combine!
    merge(A, B, L)

def merge(A, B, L):   
    i = 0 # index into A
    j = 0 # index into B
    while i < len(A) and j < len(B):
        if A[i] < B[j]:
            L[i+j] = A[i]
            i = i + 1
        else:
            L[i+j] = B[j]
            j = j + 1
    # Add any remaining elements once one list is empty
    L[i+j:] = A[i:] + B[j:]
