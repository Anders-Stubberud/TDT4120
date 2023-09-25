#!/usr/bin/python3
# coding=utf-8
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 100
# Laveste mulige antall tall i generert instans.
numbers_lower = 10
# Høyest mulig antall tall i generert instans.
numbers_upper = 100
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

import math
def k_largest(A, n, k):
    if k == 0: return []
    return select_pivot(A, 0, n, k)

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
    if r-p-x == k : return A[x:]
    if r-p-x < k : return select_pivot(A, x + 1, r, k)
    return select_pivot(A, p, x, k)

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





# Sett med hardkodete tester på format: (A, k)
tests = [
    ([], 0),
    ([1], 0),
    ([1], 1),
    ([1, 2], 1),
    ([-1, -2], 1),
    ([-1, -2, 3], 2),
    ([1, 2, 3], 2),
    ([3, 2, 1], 2),
    ([3, 3, 3, 3], 2),
    ([4, 1, 3, 2, 3], 2),
    ([4, 5, 1, 3, 2, 3], 4),
    ([9, 3, 6, 1, 7, 3, 4, 5], 4)
]

def gen_examples(k, lower, upper):
    for _ in range(k):
        A = [
                random.randint(-50, 50)
                for _ in range(random.randint(lower, upper))
            ]
        yield A, random.randint(0, len(A))


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        numbers_lower,
        numbers_upper,
    ))

failed = False
for A, k in tests:
    answer = sorted(A, reverse=True)[:k][::-1]
    student = k_largest(A[:], len(A), k)

    if type(student) != list:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Metoden må returnere en liste
Ditt svar: {student}
""")
    else:
        student.sort()
        if student != answer:
            if failed:
                print("-"*50)
            failed = True
            print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}
k: {k}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")