#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import time
start = time.time()
# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 6
# Høyest mulig antall verdier i generert instans.
# NB: Om denne verdien settes høyt (>30) kan testene ta veldig lang tid.
n_upper = 8
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 1

def minimum (x , x0 , y0 , x1 , y1 ) :
    minimal = float ("inf ")
    minimal_index = ( -1 , -1)
    for i in range ( x0 , x1 + 1) :
        for j in range ( y0 , y1 + 1) :
            if x [ i ][ j ] < minimal :
                minimal_index = (i , j )
                minimal = x [ i ][ j ]
    return minimal , minimal_index

def _largest_cuboid (x , x0 , y0 , x1 , y1 ) :
    if ( x0 , y0 ) == ( x1 , y1 ) :
        return x [ x0 ][ y0 ]
    minimal , minimal_index = minimum (x , x0 , y0 , x1 , y1 )
    maximal = ( x1 - x0 + 1) * ( y1 - y0 + 1) * minimal
    if ( x0 , y0 ) == ( x1 , y1 ) :
        return x [ x0 ][ y0 ]
    if minimal_index [0] > x0 :
        maximal = max ( maximal , _largest_cuboid (x , x0 , y0 ,minimal_index [0] - 1 , y1 ) )
    if minimal_index [0] < x1 :
        maximal = max ( maximal , _largest_cuboid (x , minimal_index [0] + 1 , y0 ,x1 , y1 ) )
    if minimal_index [1] > y0 :
        maximal = max ( maximal , _largest_cuboid (x , x0 , y0 ,x1 , minimal_index [1] - 1) )
    if minimal_index [1] < y1 :
        maximal = max ( maximal , _largest_cuboid (x , x0 , minimal_index [1] + 1 ,x1 , y1 ) )
    return maximal
def largest_cuboid ( x ) :
    return _largest_cuboid (x , 0 , 0 , len ( x ) - 1 , len ( x ) - 1)


# def largest_cuboid(x):
#     import math
#     limit = len(x) - 1
#     largest_cuboid = 0

#     def explore(x_start, x_end, y_start, y_end):
#         nonlocal largest_cuboid
#         length = y_end - y_start + 1
#         width = x_end - x_start + 1
#         depth = shallowest_depth(x_start, x_end, y_start, y_end)
#         current_cuboid = length * width * depth
#         if current_cuboid > largest_cuboid:
#             largest_cuboid = current_cuboid

#         #sjekker om det skal utforskes videre (egt bruteforce, sjekker alle rektangulære kombinasjoner)
#         if x_end < limit:
#             #kun gå videre i x-retning
#             explore(x_start, x_end+1, y_start, y_end)
#         if y_end < limit:
#             #kun videre i y-retning
#             explore(x_start, x_end, y_start, y_end+1)

#     def shallowest_depth(x_start, x_end, y_start, y_end):
#         shallowest_depth = math.inf
#         for row in range(len(x)):
#             if row < y_start: continue
#             if row > y_end: break
#             for column in range(len(x)):
#                 if column < x_start: continue
#                 if column > x_end: break
#                 if x[row][column] < shallowest_depth:
#                     shallowest_depth = x[row][column]
#         return shallowest_depth
    
#     for y_coordinate in range(len(x)):
#         for x_coordinate in range(len(x)):
#             explore(x_coordinate, x_coordinate, y_coordinate, y_coordinate)
#     end = time.time()
#     return largest_cuboid




# Hardkodete tester
tests = [
    [[1]],
    [[1, 1], [2, 1]],
    [[1, 1], [5, 1]],
    [[0, 0], [0, 0]],
    [[10, 0], [0, 10]],
    [[10, 6], [5, 10]],
    [[100, 100], [40, 55]],
]


def generate_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(nl, nu)
        yield [random.choices(range(5*n), k=n) for _ in range(n)]


# Treg bruteforce løsning for å finne løsnings for tilfeldig genererte tester.
def bruteforce_largest_cuboid(x):
    A = 0
    for B in range(len(x)):
        for C in range(len(x[0])):
            for D in range(B, len(x)):
                for E in range(C, len(x[0])):
                    h = min(min(y[C:E + 1]) for y in x[B:D+1])
                    A = max(A, (D - B + 1) * (E - C + 1) * h)
    return A


if generate_random_tests:
    if seed:
        random.seed(seed)

    tests.extend(generate_examples(random_tests, n_lower, n_upper))

failed = False
for x in tests:
    student = largest_cuboid([y[:] for y in x])
    answer = bruteforce_largest_cuboid(x)
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
end = time.time()
print(end-start)