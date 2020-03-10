def insertionsort(L):
    n = len(L)
    for i in range(n):
        for j in range(n-i-1, n-1):
            if L[j]>L[j+1]:
                L[j], L[j+1] = L[j+1], L[j]
