# !/usr/bin/python3
# coding=utf-8
import random
import math
import time
start2 = time.time()

# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 1000
# Lavest mulig antall tog i generert instans.
trains_lower = 350
# Høyest mulig antall tog i generert instans. Om denne verdien er satt høyt
# (>120), kan det ta lang tid å generere instansene.
trains_upper = 500
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 1

import math
import heapq


def earliest_arrival(timetable, start, goal):
    departures = {}  # graf over togforbindelser
    for station, destination, departure, arrival in timetable:
        if station not in departures : departures[station] = set()
        departures[station].add((destination, departure, arrival))
    heap = [(0, start)]  # min priority av ankomsttider
    arrivals = {start: 0}  # dict av ankomsttid, stasjon som key
    while heap:
        time, station = heapq.heappop(heap)
        if station == goal : return time
        if station in departures:
            for destination, departure, arrival in departures[station]:
                if ((destination not in arrivals) or (arrival < arrivals[destination])) and departure >= time:
                    arrivals[destination] = arrival
                    heapq.heappush(heap, (arrival, destination))
    return math.inf #inf dersom det ikke er mulig å komme frem


# import math
# import heapq
#
#
# class Node:
#     def __init__(self, name):
#         self.name = name
#         self.arrival = math.inf
#         self.destinations = set() #tupler (ref. node, arrivaltid)
#
#     def __lt__(self, other):
#         return self.arrival < other.arrival
#
#
# def earliest_arrival(timetable, start, goal):
#     stations = {}
#     for entry in timetable:
#         u, v = entry[0], entry[1]
#         if u not in stations : stations[u] = Node(u)
#         if v not in stations : stations[v] = Node(v)
#     for entry in timetable:
#         u, v, departure, arrival = entry[0], entry[1], entry[2], entry[3]
#         stations[u].destinations.add((stations[v], departure, arrival))
#     stations[start].arrival = 0
#     Q = [node for node in stations.values()]
#     heapq.heapify(Q)
#     while Q:
#         u = heapq.heappop(Q)
#         if u.name == goal : return u.arrival
#         for station in u.destinations:
#             destination, departure, new_arrival = station[0], station[1], station[2]
#             if destination.arrival > new_arrival and departure >= u.arrival:
#                 if destination in Q: Q.remove(destination)
#                 destination.arrival = new_arrival
#                 heapq.heappush(Q, destination)
#     return stations[goal].arrival
#
#
# import math
#
#
# def earliest_arrival(timetable, start, goal):
#     stations = {start: 0}
#     while True:
#         idle = True
#         for u, v, ud, va in timetable:
#             if u in stations and stations[u] <= ud and (v not in stations or stations[v] > va):
#                 stations[v] = va
#                 idle = False
#         if idle : break
#     return stations.get(goal, math.inf)

# Hardkodete tester på format: (tog, start, slutt), tidligst tidspunkt
tests = [
    (([("A", "B", 100, 101)], "A", "B"), 101),
    (([("B", "A", 20, 30), ("B", "A", 25, 29)], "B", "A"), 29),
    (
        ([("A", "B", 0, 10), ("B", "C", 10, 20), ("A", "C", 0, 30)], "A", "C"),
        20,
    ),
    (
        (
            [("A", "B", 0, 10), ("B", "C", 10, 20), ("A", "C", 10, 15)],
            "A",
            "C",
        ),
        15,
    ),
    (
        (
            [("A", "C", 10, 30), ("B", "C", 15, 25), ("A", "B", 0, 20)],
            "A",
            "C",
        ),
        30,
    ),
    (
        (
            [("A", "B", 10, 30), ("B", "C", 15, 25), ("B", "C", 35, 50)],
            "A",
            "C",
        ),
        50,
    ),
    (
        (
            [("A", "B", 10, 30), ("B", "C", 30, 40), ("B", "C", 35, 50)],
            "A",
            "C",
        ),
        40,
    ),
    (
        (
            [("Y", "C", 43, 98), ("C", "Y", 17, 61), ("Y", "C", 13, 18)],
            "Y",
            "C",
        ),
        18,
    ),
    (([("T", "M", 93, 97)], "T", "M"), 97),
    (
        (
            [
                ("G", "Z", 62, 79),
                ("P", "Z", 96, 98),
                ("G", "P", 87, 96),
                ("G", "P", 1, 52),
                ("G", "P", 66, 93),
            ],
            "G",
            "Z",
        ),
        79,
    ),
    (
        (
            [
                ("B", "X", 48, 97),
                ("X", "Q", 1, 19),
                ("B", "X", 22, 42),
                ("X", "Q", 2, 35),
                ("B", "X", 63, 78),
            ],
            "B",
            "X",
        ),
        42,
    ),
    (([("W", "R", 41, 58)], "W", "R"), 58),
    (
        (
            [
                ("U", "L", 53, 58),
                ("U", "A", 68, 88),
                ("L", "U", 80, 82),
                ("U", "L", 47, 90),
            ],
            "U",
            "L",
        ),
        58,
    ),
    (([("O", "X", 44, 73)], "O", "X"), 73),
    (
        (
            [
                ("D", "R", 64, 80),
                ("D", "X", 24, 59),
                ("D", "X", 25, 90),
                ("D", "R", 33, 84),
                ("R", "D", 72, 83),
            ],
            "D",
            "R",
        ),
        80,
    ),
    (
        (
            [
                ("X", "P", 32, 95),
                ("X", "P", 89, 99),
                ("X", "P", 28, 93),
                ("P", "X", 76, 96),
            ],
            "P",
            "X",
        ),
        96,
    ),
    (
        (
            [("G", "Y", 22, 94), ("L", "G", 7, 61), ("G", "Y", 96, 98)],
            "G",
            "Y",
        ),
        94,
    ),
    (
        (
            [
                ("A", "B", 0, 4),
                ("B", "C", 4, 7),
                ("A", "C", 0, 15),
                ("B", "D", 4, 13),
                ("C", "D", 8, 11),
            ],
            "A",
            "D",
        ),
        11
    )
]


# Treg bruteforce løsning
def slow_solve(timetable, start, goal):
    return earliest_arrival(timetable, start, goal)


def gen_examples(k, nl, nu):
    for _ in range(k):
        n = random.randint(max(1, nl), nu)
        ns = random.randint(5, max(5, math.log(n, 20)))
        stations = set()
        while len(stations) < ns:
            stations.add(
                "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                                       k=math.ceil(math.log(ns, 20))))
            )
        stations = tuple(stations)

        T = []
        for _ in range(n):
            t0 = random.randint(0, 10 * n)
            t1 = random.randint(t0 + 1, t0 + 1 * n)
            T.append((
                *random.sample(stations, k=2),
                t0,
                t1
            ))

        s, g = random.sample(stations, k=2)
        while slow_solve(T, s, g) == float("inf"):
            s, g = random.sample(stations, k=2)

        check = lambda d, e, f: any(a == d and b == e and t1 == f for a, b, _, t1 in T)

        if check(s, g, slow_solve(T, s, g)):
            for _ in range(20):
                x, y = random.sample(stations, k=2)
                if not check(x, y, slow_solve(T, x, y)):
                    s, g = x, y
                    break
        yield (T, s, g), slow_solve(T, s, g)


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        trains_lower,
        trains_upper,
    ))

failed = False
for test_case, answer in tests:
    timetable, start, goal = test_case
    student = earliest_arrival(timetable[:], start, goal)
    if student != answer:
        if failed:
            print("-" * 50)
        failed = True
        print(f"""
Koden feilet for følgende instans.
start: {start}
goal: {goal}
timetable:
    {(chr(10) + '    ').join(f"{a} -> {b} (reiser {t_0}, fremme {t_1})" for a, b, t_0, t_1 in timetable)}

Ditt svar: {student}
Riktig svar: {answer}
""")

if not failed:
    print("Koden fungerte for alle eksempeltestene.")

end = time.time()
print(end - start2)