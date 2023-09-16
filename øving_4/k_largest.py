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

    
def k_largest(A, n, k):
    import random
    if k == 0: return []

    def randomized_partition_providing_index_of_pivot(liste, p, r):
        random_index = random.randint(p, r) 
        pivot_element = liste[random_index]
        liste[random_index], liste[r] = liste[r], liste[random_index]
        swap = p - 1
        for i in range(p, r):
            if liste[i] <= pivot_element:
                swap += 1
                liste[i], liste[swap] = liste[swap], liste[i]
        liste[swap + 1], liste[r] = liste[r], liste[swap + 1]
        return swap + 1

    def randomized_select(A, p, r, i):
        pivot_index = randomized_partition_providing_index_of_pivot(A, p, r)
        big_elements_partitioned = r - pivot_index + 1
        if i == big_elements_partitioned: return A[pivot_index]
        if i < big_elements_partitioned: 
            return randomized_select(A, pivot_index+1, r, i)
        else:
            return randomized_select(A, p, pivot_index-1, i - big_elements_partitioned)

    randomized_select(A, 0, n-1, k)

    return A[n-k:]
            




    # if k == 0: return []
    # while n % 5 != 0:
    #     if k == n: return A
    #     for i in range(1, n):
    #         if A[i] < A[0]:
    #             A[0], A[i] = A[i], A[0]
    #     A.pop(0)
    #     n -= 1
    # g = int(n / 5)
    # for i in range(g):
    #     sort_in_place([i, i+g, i+2*g, i+3*g, i+4*g])
    # x = k_largest(A[2*g:3*g], 3*g-2*g, int(g/2))
    # q = partition(A[2*g:3*g], x)
    # k_th_smallest = q + 1
    # if k == k_th_smallest:
    #     return A[q:]
    # if k < k_th_smallest:
    #     arr = A[:k_th_smallest]
    #     return k_largest(arr, len(arr), k)
    # else:
    #     arr = A[k_th_smallest+1:]
    #     k = k - len(A[k_th_smallest+1:])
    #     return k_largest(arr, len(arr), k)

    



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