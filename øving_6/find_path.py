#!/usr/bin/python3
# coding=utf-8
import random
import math
import time

start = time.time()


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 30
# Laveste mulige antall tall i hver kolonne og rad i generert instans.
numbers_lower = 7
# Høyest mulig antall tall i hver kolonne og rad i generert instans.
# NB: Om denne verdien settes høyt (>15) vil det ta veldig lang tid å
# generere testene.
numbers_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 1


def find_path(weights):
    dybde = len(weights)
    lengde = len(weights[0])
    sti = {}
    for d in range(1, dybde):
        for l in range(lengde):
            retning = 0
            verdi_retning = weights[d-1][l]
            if l != 0 and weights[d-1][l-1] < verdi_retning:
                retning = -1
                verdi_retning = weights[d-1][l-1]
            if l != lengde-1 and weights[d-1][l+1] < verdi_retning:
                retning = 1
                verdi_retning = weights[d-1][l+1]
            sti[(l, d)] = (l+retning, d-1)
            weights[d][l] += weights[d-1][l+retning]
    minste = math.inf
    enden = None
    for i in range(lengde):
        if weights[dybde-1][i] < minste:
            minste = weights[dybde-1][i]
            enden = (i, dybde - 1)
    res = [None] * dybde
    res[dybde-1] = enden
    elm = enden
    for i in range(dybde-2, -1, -1):
        elm = sti[elm]
        res[i] = elm
    return res



# Hardkodete tester
tests = [
    [[1]],
    [[1, 1]],
    [[1], [1]],
    [[2, 1], [2, 1]],
    [[1, 1], [1, 1]],
    [[2, 1], [1, 2]],
    [[3, 2, 1], [1, 3, 2], [2, 1, 3]],
    [[1, 9, 3, 3], [1, 9, 3, 3], [9, 9, 3, 3]],
    [[1, 2, 7, 4], [9, 3, 2, 5], [5, 7, 8, 3], [1, 3, 4, 6]],
]

# Treg bruteforce løsning for å finne vekten til den optimale stien
def bruteforce(w, i=None, j=0):
    if i is None:
        return min(bruteforce(w, i)
                   for i in range(len(w[0])))

    if j == len(w):
        return 0

    best = float("inf")
    if i > 0:
        best = min(best, bruteforce(w, i - 1, j + 1))
    best = min(best, bruteforce(w, i, j + 1))
    if i < len(w[0]) - 1:
        best = min(best, bruteforce(w, i + 1, j + 1))

    return w[j][i] + best


# Verifiserer at en løsning er riktig gitt vektene, stien og den minst
# mulige vekten man kan ha på en sti.
def verify(weights, path, optimal):
    if path is None:
        return False, "Svaret er ikke en sti"

    if len(path) != len(weights):
        return False, "Stien er enten for lang eller for kort."

    last = -1
    for index, element in enumerate(path):
        if type(element) != tuple:
            return False, "Stien består ikke av tupler."
        if len(element) != 2:
            return False, "Stien består ikke av tupler på formatet (x,y)."
        if index != element[1]:
            return False, "Stien er ikke vertikal."
        if element[0] < 0 or element[0] >= len(weights[0]):
            return False, "Stien går utenfor bildet."
        if last != -1 and not last - 1 <= element[0] <= last + 1:
            return False, "Stien hopper mer enn en piksel per rad."
        last = element[0]

    weight = sum(weights[y][x] for x, y in path)
    if weight != optimal:
        return (
            False,
            "Stien er ikke optimal. En optimal sti ville hatt"
            + "vekten {:}, mens din hadde vekten {:}".format(optimal, weight),
        )

    return True, ""


def gen_examples(k, lower, upper):
    for _ in range(k):
        w, h = random.randint(lower, upper), random.randint(lower, upper)
        yield [[random.randint(0, 9) for _ in range(w)] for _ in range(h)]


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        numbers_lower,
        numbers_upper,
    ))


failed = False

for test in tests:
    student = find_path([row[:] for row in test])
    optimal_weight = bruteforce(test)
    correct, error_message = verify(test, student, optimal_weight)
    if not correct:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
weights:
{chr(10).join(["  ".join(map(str, row)) for row in test])}

Ditt svar: {student}
Feilmelding: {error_message}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")

end = time.time()
print(end-start)
