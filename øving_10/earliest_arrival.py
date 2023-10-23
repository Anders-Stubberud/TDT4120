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
random_tests = 100
# Lavest mulig antall tog i generert instans.
trains_lower = 10
# Høyest mulig antall tog i generert instans. Om denne verdien er satt høyt
# (>120), kan det ta lang tid å generere instansene.
trains_upper = 100
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 1

def earliest_arrival(timetable, start, goal):
    stations = {}
    for entry in timetable:
        u, v = entry[0], entry[1]
        stations[u], stations[v] = math.inf, math.inf
    stations[start] = 0
    for _ in range(len(stations)):
        idle = True
        for entry in timetable:
            u, v, ud, va = entry[0], entry[1], entry[2], entry[3]
            if stations[u] <= ud and stations[v] > va:
                stations[v] = va 
                idle = False
        if idle : break
    return stations[goal]


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
def slow_solve(T, s, g, t=0):
    if s == g:
        return t
    m = float("inf")
    for a, b, t0, t1 in T:
        if a == s and t0 >= t:
            m = min(slow_solve(T, b, g, t1), m)
    return m


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
            t0 = random.randint(0, 10*n)
            t1 = random.randint(t0 + 1, t0 + 1*n)
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
            print("-"*50)
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
print(type(start2))
print(type(end))
print(end-start2)