#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres
random_tests = 100
# Lavest mulig antall verdier i generert instans.
n_lower = 10
# Høyest mulig antall verdier i generert instans.
n_upper = 100
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0


def find_maximum(x):
    first_index = 0
    end_index = len(x) - 1

    def backtrack(start, end):
        middle = int((start+end)/2)
    #basecaser
        #kun 1 element igjen; dette må da være størst
        if start == end:
            return x[middle]
        #dersom middle er størst
        if x[middle-1]<x[middle] and x[middle]>x[middle+1]:
            return x[middle]
    #rekursjon til halvdel med største element
        if x[start]>x[middle] and x[middle]<x[end]:
            return backtrack(start, middle-1) if x[start]>x[end] else backtrack(middle+1, end)
        return backtrack(start, middle-1) if x[middle-1]>x[middle+1] else backtrack(middle+1, end)

    return backtrack(first_index, end_index)


# Hardkodete tester på format: (x, svar)
tests = [
    ([1], 1),
    ([1, 3], 3),
    ([3, 1], 3),
    ([1, 2, 1], 2),
    ([1, 0, 2], 2),
    ([2, 0, 1], 2),
    ([0, 2, 1], 2),
    ([0, 1, 2], 2),
    ([2, 1, 0], 2),
    ([2, 3, 1, 0], 3),
    ([2, 3, 4, 1], 4),
    ([2, 1, 3, 4], 4),
    ([4, 2, 1, 3], 4),
]


# Genererer tilfeldige instanser med svar
def generate_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        x = random.sample(range(5*n), k=n)
        answer = max(x)
        t = x.index(answer)
        x = sorted(x[:t]) + [answer] + sorted(x[t + 1:], reverse=True)
        t = random.randint(0, n)
        x = x[t:] + x[:t]
        yield x, answer


if generate_random_tests:
    if seed:
        random.seed(seed)

    tests.extend(generate_examples(random_tests, n_lower, n_upper))


failed = False
for x, answer in tests:
    student = find_maximum(x[:])
    if student != answer:
        if failed:
            print("-"*50)

        failed = True

        print(f"""
Koden ga feil svar for følgende instans:
x: {x}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")