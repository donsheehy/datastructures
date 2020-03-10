def quicksorted(L):
    #base case
    if len(L) < 2:
        return L[:]

    # Divide!
    pivot = L[-1]
    LT = [e for e in L if e < pivot]
    ET = [e for e in L if e == pivot]
    GT = [e for e in L if e > pivot]

    # Conquer
    A = quicksorted(LT)
    B = quicksorted(GT)

    # Combine
    return A + ET + B

def quicksort(L, left = 0, right = None):
    if right is None:
        right = len(L)

    if right - left > 1:    
        # Divide!
        mid = partition(L, left, right)

        # Conquer!
        quicksort(L, left, mid)
        quicksort(L, mid+1, right)

        # Combine!
        # Nothing to do!

def partition(L, left, right):
    pivot = right - 1
    i = left        # index in left half
    j = pivot - 1   # index in right half

    while i < j:
        # Move i to point to an element >= L[pivot]
        while L[i] < L[pivot]:
            i = i + 1

        # Move j to point to an element < L[pivot]
        while i < j and L[j] >= L[pivot]:
            j = j - 1

        # Swap elements i and j if i < j
        if i < j:
            L[i], L[j] = L[j], L[i]

    # Put the pivot in place.
    if L[pivot] <= L[i]:
        L[pivot], L[i] = L[i], L[pivot]
        pivot = i

    # Return the index of the pivot.
    return pivot
