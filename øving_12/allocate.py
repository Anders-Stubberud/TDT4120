#!/usr/bin/python3
# coding=utf-8
from math import ceil
import random
import itertools
from collections import deque
from typing import List, Optional, Tuple


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall agenter i generert instans.
agents_lower = 3
# Høyest mulig antall agenter i generert instans.
# NB: Om denne verdien settes høyt (>25) kan det ta veldig lang tid å
# generere testene.
agents_upper = 8
# Laveste mulige antall gjenstander i generert instans.
items_lower = 3
# Høyest mulig antall gjenstander i generert instans.
# NB: Om denne verdien settes høyt (>25) kan det ta veldig lang tid å
# generere testene.
items_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

def allocate(categories, valuations, n, m) -> List[List[int]]:
    c = len(categories)
    source, sink = 0, 1 + n + n * c + m
    nodes = sink + 1
    capacities = [[0 for i in range(sink + 1)] for _ in range(sink + 1)]
    for h, i in enumerate(range(1, n * (1 + c) + 2 - c, c + 1)):  # h er person, i er index til person h
        desire = ceil(len(valuations[h]) / n)
        capacities[0][i] = desire  # edge fra source til alle personer
        for g, j in enumerate(range(i + 1, i + c + 1)):  # j er innført kategori node
            capacities[i][j] = categories[j - (i + 1)][0]  # edge fra person til gitt kategori
            for l, k in enumerate(range(1 + n * (1 + c), sink)):  # l er item, k er index til item l i matrisen
                capacities[j][k] = 1 if l in valuations[h] and l in categories[g][1] else 0
                capacities[k][sink] = 1
    flow = max_flow(source, sink, nodes, capacities)
    res = [[] for _ in range(n)]  # item-liste for hver person
    for k, i in enumerate(range(1 + n * (1 + c), sink)):  # i er index til item i matrisen
        for j in range(nodes):  # j er index til kategori av person som har item dersom -1
            if flow[i][j] == -1: res[(j - 1) // (c + 1)].append(k)
    for i in range(n):
        if len(res[i]) < ceil(len(valuations[i]) / n) : return None
    return res


def max_flow(
        source: int, sink: int, nodes: int, capacities: List[List[int]]
) -> List[List[int]]:
    flows = [[0] * nodes for _ in range(nodes)]
    augmenting_path = find_augmenting_path(source, sink, nodes, flows, capacities)
    while augmenting_path:
        residual_capacity = max_path_flow(augmenting_path, flows, capacities)
        send_flow(augmenting_path, residual_capacity, flows)
        augmenting_path = find_augmenting_path(source, sink, nodes, flows, capacities)
    return flows


def find_augmenting_path(
        source: int,
        sink: int,
        nodes: int,
        flows: List[List[int]],
        capacities: List[List[int]],
) -> Optional[List[int]]:
    def create_path(source: int, sink: int, parent: List[int]) -> List[int]:
        node = sink
        path = [sink]
        while node != source:
            node = parent[node]
            path.append(node)
        path.reverse()
        return path

    discovered = [False] * nodes
    parent = [0] * nodes
    queue = deque()
    queue.append(source)

    while queue:
        node = queue.popleft()
        if node == sink:
            return create_path(source, sink, parent)

        for neighbour in range(nodes):
            if (
                    not discovered[neighbour]
                    and flows[node][neighbour] < capacities[node][neighbour]
            ):
                queue.append(neighbour)
                discovered[neighbour] = True
                parent[neighbour] = node
    return None


def max_path_flow(
        path: List[int], flows: List[List[int]], capacities: List[List[int]]
) -> int:
    flow = float("inf")
    for i in range(1, len(path)):
        u, v = path[i - 1], path[i]
        flow = min(flow, capacities[u][v] - flows[u][v])
    return flow


def send_flow(path: List[int], flow: float, flows: List[List[float]]):
    for i in range(1, len(path)):
        u, v = path[i - 1], path[i]
        flows[u][v] += flow
        flows[v][u] -= flow


# Hardkodete tester på format:
# (kategorier, verdifunksjoner, n, m, eksisterer det en proporsjonal allokasjon)
tests = [
    (((1, (0, 1)), (2, (2, 3))),
     ([0, 2, 3], [0, 2]),
     2,
     4,
     True,
    ),
    (((1, (0, 1)),),
     ([0, 1], [0, 1]),
     2,
     2,
     True,
    ),
    (((2, (0, 1, 2)),),
     ([0, 1, 2], [0, 1, 2]),
     2,
     3,
     False,
    ),
    (((2, (0, 1, 2, 3)),),
     ([0, 1, 2, 3], [0, 1, 2, 3]),
     2,
     4,
     True,
    ),
    (((2, (0, 1, 2, 3)),),
     ([0, 1, 3], [0, 1, 3]),
     2,
     4,
     False,
    ),
    (((2, (0, 1, 2)), (1, (3,))),
     ([0, 1, 2, 3], [0, 1, 2, 3]),
     2,
     4,
     True,
    ),
    (((2, (0, 1, 2)), (1, (3,))),
     ([0, 1, 3], [0, 1, 3]),
     2,
     4,
     False,
    ),
    (((2, (0, 1, 2)), (1, (3, 5)), (1, (4,))),
     ([1, 2, 4, 5], [1, 2, 4, 5]),
     2,
     6,
     True,
    ),
]


def check_recursive(categories, likes, req, i, remaining):
    if i == len(likes):
        return True

    choices = remaining & likes[i]
    if len(choices) < req[i]:
        return False

    for comb in itertools.combinations(choices, req[i]):
        comb = set(comb)
        for threshold, items in categories:
            if len(comb & set(items)) > threshold:
                break
        else:
            if check_recursive(categories, likes, req, i + 1, remaining - comb):
                return True

    return False


# Treg bruteforce løsning
def bruteforce_solve(categories, valuations, n, m):
    req = [ceil(len(valuation)/n) for valuation in valuations]
    return check_recursive(categories, valuations, req, 0, set(range(m)))


def gen_examples(k, nl, nu, ml, mu):
    for _ in range(k):
        n = random.randint(nl, nu)
        m = random.randint(ml, mu)
        c = random.randint(1, m)

        boundaries = [0] + sorted([random.randint(0, m) for _ in range(c-1)]) + [m]
        categories = []
        items = list(range(m))
        random.shuffle(items)
        for a, b in zip(boundaries, boundaries[1:]):
            category_items = items[a:b]
            categories.append((random.randint(1, max(len(category_items), 1)),
                               tuple(category_items)))
        categories = tuple(categories)

        val_function = lambda L: lambda x: x in L

        valuations = [
                random.sample(items, random.randint(0, m))
                for _ in range(n)
        ]

        exists = bruteforce_solve(categories, valuations, n, m)

        yield categories, valuations, n, m, exists


if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(
        random_tests,
        agents_lower,
        agents_upper,
        items_lower,
        items_upper,
    ))

def verify(m, categories, valuations, exists, student):
    if not exists:
        if student is not None:
            return "Du returnert ikke None selv om det ikke finnes en proporsjonal allokasjon."
        return None

    if type(student) != type([]):
        return "Du returnerte ikke en liste."

    if len(student) != len(valuations):
        return "Svaret inneholder ikke nøyaktig en samling med gjenstander for hver agent."

    # Test that each agent has a list as a bundle
    if any(type(bundle) != type([]) for bundle in student):
        return "En av samlingene med gjenstander er ikke en liste."

    # Test type of each item
    if any(type(item) != int for bundle in student for item in bundle):
        return "Du har returnert en gjenstand som ikke finnes."

    # Test that each item in each bundle is an item
    if not all(0 <= item < m for bundle in student for item in bundle):
        return "Du har returnert en gjenstand som ikke finnes."

    # Test that each item appears at most once in each bundle
    if any(len(set(bundle)) < len(bundle) for bundle in student):
        return "En samling inneholder samme gjenstand flere ganger."

    # Test that some item has not been allocated multiple times
    for i in range(len(valuations)):
        for j in range(i + 1, len(valuations)):
            if set(student[i]) & set(student[j]):
                return "Hver gjenstand kan kun gis til en av personene."

    # Test that each agent does not receive more than threshold items from
    # each category multiple items
    for bundle in student:
        for threshold, category in categories:
            if len(set(bundle) & set(category)) > threshold:
                print(threshold, category, bundle)
                return "En samling innholder flere gjenstander fra en kategori enn er lov."

    for valuation, bundle in zip(valuations, student):
        if len(set(valuation) & set(bundle)) < ceil(len(valuation) / len(valuations)):
            return "En person har ikke fått gjenstander med nok verdi."


def format_valuations(valuations, m):
    string = ""
    for i, valuation in enumerate(valuations):
        string += f"    Agent {i}: {valuation}\n"
    return string


failed = False
for categories, valuations, n, m, exists in tests:
    student = allocate(categories, [val[:] for val in valuations], n, m)
    feedback = verify(m, categories, valuations, exists, student)

    if feedback is not None:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
n: {n}
m: {m}
categories: {categories}
valuations:
{format_valuations(valuations, m)}
Ditt svar: {student}
Feilmelding: {feedback}
""")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
