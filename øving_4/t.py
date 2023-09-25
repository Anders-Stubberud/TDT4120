import math
def k_largest(A, n, k):
    if k == 0 : return []
    ind = select_pivot(A, 0, n, k)
    return A[ind+1:]

def select_pivot(A, p, r, k):
    while (r-p) % 5 != 0:
        for i in range(p+1, r):
            if A[p] > A[i]: A[p], A[i] = A[i], A[p]
        #returnerer index til pivot
        if k == 1 : return p
        p += 1
        k -= 1
    groups = int((r-p)/5)
    for i in range(groups) : insertion_sort_modified(A, [i, i + groups,i + 2*groups, i + 3*groups, i + 4*groups])
    #x er nå indexen til pivot
    x = select_pivot(A, p + 2*groups, p + 3*groups, math.ceil(groups/2))
    partition(A, p, r, x)
    order = x - p + 1
    if order == k : return x
    if order > k : return select_pivot(A, p, x, k)
    return select_pivot(A, x+1, r, k)

def partition(A, p, r, x):
    pivot = A[x]
    #setter pivot bakerst
    A[x], A[r-1] = A[r-1], A[x]
    j = p - 1
    for i in range(p, r - 1):
        if A[i] <= pivot:
            j += 1
            A[j], A[i] = A[i], A[j]
    A[j + 1], A[r-1] = A[r-1], A[ j + 1]


def insertion_sort_modified(A, arr):
    for i in range(1,5):
        #A[arr[i]] blir skrevet over, dermed må den lagres i variabel
        key = A[arr[i]]
        j = i - 1
        while j >= 0 and key < A[arr[j]]:
            A[arr[j + 1]] = A[arr[j]]
            j -= 1
        A[arr[j+1]] = key

A = [5,4,3,2,1]
n = 4
k = 2
print(k_largest(A, n, k))

