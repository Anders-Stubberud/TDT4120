 #!/usr/bin/python3
# coding=utf-8
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres
random_tests = 50
# Lavest mulig antall verdier i generert instans.
n_lower = 100
# Høyest mulig antall verdier i generert instans.
n_upper = 200
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def insertion_sort(A, n):
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and key < A[j]:
            A[ j + 1 ] = A[ j ]
            j -= 1
        A[ j + 1 ] = key
    return A


# Hardkodete tester
tests = [
    [],
    [1, 2, 3],
    [3, 2, 1],
    [9, 7, 3, 5, 2, 6],
    [-1, 1, -1, 2],
    [-5, 8, 3, 10, 2, 15],
]


# Genererer k tilfeldige tester, hver med et tilfeldig antall elementer plukket
# uniformt fra intervallet [nl, nu].
def gen_examples(k, nl, nu):
    for _ in range(k):
        yield [random.randint(-99, 99) for _ in range(random.randint(nl, nu))]


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(random_tests, n_lower, n_upper))

failed = False
for A in tests:
    answer = sorted(A)
    student = insertion_sort(A[:], len(A))
    if student != answer:
        if failed:
            print("-"*50)
        failed = True

        print(f"""
Koden feilet for følgende instans:
A: {A}
n: {len(A)}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")