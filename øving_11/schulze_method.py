# !/usr/bin/python3
# coding=utf-8


# De lokale testene består av to deler. Et lite sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å teste på
# et større sett med 500 genererte instanser. For å teste på det
# større settet med genererte instanser, må du (1) laste ned filen med
# testene fra øvingssystemet, (2) legge den samme plass som denne
# python-filen og (3) sette variabelen under til True. Merk at det kan
# ta litt tid å kjøre alle de 500 ekstra testene.
use_extra_tests = True


# finner maksimal styrke i,j ved input av 1-directed-edge-per-par-matrise
def modified_floyd_warshall(D, n):
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if i == j : continue
                D[i][j] = max(D[i][j], min(D[i][k], D[k][j]))


def schulze_method(A, n):
    E, C, res = [[0 for _ in range(n)] for _ in range(n)], {i for i in range(n)}, []  # init Edges, Contestants, resultat
    for i in range(n):  # setter opp matrise med 1 directed edge per par av noder
        for j in range(n):
            if (A[i][j] > A[j][i]) or (A[i][j] == A[j][i] and i < j) : E[i][j] = A[i][j]
    modified_floyd_warshall(E, n)  # maksimal styrke for hvert par av noder
    for _ in range(n):  # velger ut en contestant per iterasjon
        leader_contestant, leader_score, already_added = None, -1, False
        for u in range(n):  # undersøker om hver u opprettholder p(u, v) > p(v, u)
            if u not in C : continue
            valid_max_strength_for_all_edges, score = True, 0
            for v in range(n):
                if u == v or v not in C : continue
                if E[v][u] > E[u][v]:
                    valid_max_strength_for_all_edges = False
                    break
                if E[u][v] == E[v][u]: valid_max_strength_for_all_edges = False
                else : score += 1
            if valid_max_strength_for_all_edges:  # dersom p(u, v) > p(v, u) for alle v, så legges u til i resultatet
                res.append(u), C.remove(u)
                already_added = True
                break
            if score > leader_score : leader_contestant, leader_score = u, score  # ellers, dersom flest p(u, v) > p(v, u)
        if not already_added : res.append(leader_contestant), C.remove(leader_contestant)
    return res



# Hardkodete tester på format: (A, svar)
tests = [
    ([[0]], [0]),
    ([[0, 1], [3, 0]], [1, 0]),
    ([[0, 2], [2, 0]], [0, 1]),
    ([[0, 4, 3], [2, 0, 2], [3, 4, 0]], [0, 2, 1]),
    ([[0, 2, 1], [4, 0, 4], [5, 2, 0]], [1, 2, 0]),
    (
        [
            [0, 1, 3, 3, 3],
            [9, 0, 5, 5, 7],
            [7, 5, 0, 5, 4],
            [7, 5, 5, 0, 6],
            [7, 3, 6, 4, 0],
        ],
        [1, 3, 4, 2, 0],
    ),
    (
        [
            [0, 6, 7, 8, 7, 8],
            [6, 0, 6, 8, 7, 8],
            [5, 6, 0, 6, 5, 7],
            [4, 4, 6, 0, 5, 6],
            [5, 5, 7, 7, 0, 6],
            [4, 4, 5, 6, 6, 0],
        ],
        [0, 1, 4, 2, 3, 5],
    ),
]


def validate(student, answer):
    try:
        len(student)
    except:
        return "Koden returnerte ikke en liste"

    if len(student) != len(answer):
        return "Listen inneholder ikke riktig antall kandidater"

    if set(student) != set(answer):
        return "Listen inneholder ikke alle kandidatene"

    if any(a != b for a, b in zip(student, answer)):
        return "En eller flere av kandidatene opptrer i feil rekkefølge"


def generate_feedback(test, expected, student):
    feedback = ""
    feedback += "Koden din feilet for input\n"
    feedback += str(test) + "\n"
    feedback += "Ditt svar er\n"
    feedback += str(student) + ",\n"
    feedback += "men riktig svar er\n"
    feedback += str(expected) + "."
    return feedback


table_format = lambda T: "\n    " + "\n    ".join(map(str, T))
failed = False
for A, answer in tests:
    student = schulze_method([row[:] for row in A], len(A))
    feedback = validate(student, answer)
    if feedback is not None:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans.
A: {table_format(A)}
n: {len(A)}

Ditt svar: {student}
Riktig svar: {answer}
Feedback: {feedback}
""")

if use_extra_tests:
    with open("tests_schulze_method.txt") as extra_tests_data:
        extra_tests = []
        for line in extra_tests_data:
            A, answer = map(eval, line.strip().split(" | "))
            extra_tests.append((A, answer))

    n_failed = 0
    for A, answer in extra_tests:
        student = schulze_method([row[:] for row in A], len(A))
        feedback = validate(student, answer)
        if feedback is not None:
            n_failed += 1
            if failed and n_failed <= 5:
                print("-"*50)

            failed = True
            if n_failed <= 5:
                print(f"""
Koden feilet for følgende instans.
A: {table_format(A)}
n: {len(A)}

Ditt svar: {student}
Riktig svar: {answer}
Feedback: {feedback}
""")
            elif n_failed == 6:
                print("Koden har feilet for mer enn 5 av de ekstra testene.")
                print("De resterende feilene vil ikke skrives ut.")

    if n_failed > 0:
        print(f"Koden feilet for {n_failed} av de ekstra testene.")

if not failed:
    print("Koden din passerte alle eksempeltestene.")