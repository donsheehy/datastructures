def selectionsort(L):
    n = len(L)
    for i in range(n-1):
        max_index=0        
        for index in range(n - i):
            if L[index] > L[max_index]:
                max_index = index
        L[n-i-1], L[max_index] = L[max_index], L[n-i-1]
