# !/usr/bin/python3
# coding=utf-8
import time
start = time.time()

# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 1000 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True.
from calendar import c


use_extra_tests = True

class Node:
    def __init__(self, var_set) -> None:
        self.members = var_set
        self.parent = self
        self.constraints = set()
        self.rank = 0

def check(variables, constraints):
    forest = set()
    mapper = {}
    for variable in variables:
        node = Node({variable})
        mapper[variable] = node
        forest.add(node)
    def get_parent(node):
        if node != node.parent:
            node.parent = get_parent(node.parent)
        return node.parent
    for constraint in constraints:
        sign = constraint[1]
        parent_left, parent_right = get_parent(mapper[constraint[0]]), get_parent(mapper[constraint[2]])
        if sign == '=':
            if parent_left != parent_right:
                node = parent_left if parent_left.rank > parent_right.rank else parent_right
                node.members = parent_left.members.union(parent_right.members)
                node.constraints = parent_left.constraints.union(parent_right.constraints)
                parent_left.parent, parent_right.parent = node, node
                forest.remove(parent_left)
                forest.remove(parent_right)
                forest.add(node)
        elif sign == '<': parent_left.constraints.add(parent_right)
        elif sign == '>': parent_right.constraints.add(parent_left)
    valid = set()
    def cycle(node, path):
        if node in path: return True
        path.add(node)
        for con in node.constraints:
            if con in valid : continue
            if cycle(get_parent(con), path): return True
        valid.add(node)
        path.remove(node)
        return False
    while forest:
        node = forest.pop()
        if cycle(node, set()) : return False
    return True


# Hardkodete tester på format: (variables, constraints), riktig svar
tests = [
    ((["x1"], []), True),
    ((["x1", "x2"], [("x1", "=", "x2")]), True),
    ((["x1"], [("x1", ">", "x1")]), False),
    ((["x1"], [("x1", "=", "x1")]), True),
    ((["x1", "x2"], [("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x2", "<", "x1"), ("x1", "=", "x2")]), False),
    ((["x1", "x2"], [("x2", ">", "x1"), ("x1", "<", "x2")]), True),
    ((["x1", "x2"], [("x1", ">", "x2"), ("x2", ">", "x1")]), False),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x2", "<", "x3"), ("x1", ">", "x3")],
        ),
        False,
    ),
    (
        (
            ["x1", "x2", "x3"],
            [("x1", "<", "x2"), ("x3", "=", "x1"), ("x2", "<", "x3")],
        ),
        False,
    ),
    ((["x4", "x0", "x1"], [("x1", "<", "x0")]), True),
    ((["x5", "x8"], [("x8", "<", "x5"), ("x8", "<", "x5")]), True),
    ((["x1", "x0", "x2"], []), True),
    (
        (
            ["x4", "x8", "x5"],
            [("x4", "<", "x5"), ("x8", ">", "x5"), ("x5", "<", "x8")],
        ),
        True,
    ),
    (
        (
            ["x5", "x9", "x0"],
            [
                ("x9", ">", "x5"),
                ("x9", "=", "x0"),
                ("x0", "=", "x9"),
                ("x0", "=", "x9"),
            ],
        ),
        True,
    ),
    (
        (
            ["x0", "x6", "x7"],
            [("x7", "=", "x0"), ("x7", ">", "x0"), ("x6", ">", "x0")],
        ),
        False,
    ),
    ((["x8", "x6", "x0"], []), True),
    (
        (
            ["x8", "x7", "x0"],
            [("x8", "=", "x0"), ("x0", "=", "x8"), ("x0", "=", "x8")],
        ),
        True,
    ),
    (
        (
            ["x8", "x4"],
            [
                ("x4", ">", "x8"),
                ("x4", ">", "x8"),
                ("x8", "<", "x4"),
                ("x4", ">", "x8"),
                ("x8", "=", "x4"),
            ],
        ),
        False,
    ),
    ((["x3", "x8", "x5"], [("x3", ">", "x8")]), True),
]


failed = False
for test_case, answer in tests:
    variables, constraints = test_case
    student = check(variables, constraints)
    if student != answer:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
""")

if use_extra_tests:
    with open("tests_theory_solver.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            variables, constraints, answer = line.strip().split(" | ")
            variables = variables.split(",")
            constraints = [x.split(" ") for x in constraints.split(",")]
            extra_tests.append(((variables, constraints), bool(int(answer))))

    n_failed = 0
    for test_case, answer in extra_tests:
        variables, constraints = test_case
        student = check(variables, constraints)
        if student != answer:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for følgende instans:
variables: {', '.join(variables)}
constraints:
    {(chr(10) + '    ').join(' '.join(x) for x in constraints)}

Ditt svar: {student}
Riktig svar: {answer}
""")
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")

end = time.time()
print(end - start)