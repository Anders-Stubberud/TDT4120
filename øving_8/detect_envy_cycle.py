from itertools import permutations
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nedre, og muligheten for å generere
# tilfeldige instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å justere på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = True
# Antall tilfeldige tester som genereres.
random_tests = 10
# Laveste mulige antall agenter i generert instans.
n_lower = 5
# Høyest mulig antall agenter i generert instans.
# NB: Om dette antallet settes høyt vil det ta veldig lang tid å kjøre
# testene, da mulige svar sjekkes ved bruteforce.
n_upper = 6
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0

def detect_envy_cycle(n, values):
    discovered = []
    for i in range(n):
        envy_cycle = dfs(i, [], discovered, values, n)
        if envy_cycle: return envy_cycle
    return None

def dfs(i, arr, discovered, values, n):
    _envies_ = envies(i, values, n)
    for envy in _envies_:
        if envy in arr: return arr[arr.index(envy):]
        if not envy in discovered:
            arr.append(envy)
            val = dfs(envy, arr, discovered, values, n)
            if val: return val 
            arr.pop()
    discovered.append(i)
    return None
    
def envies(i, values, n):
    res = []
    val = values[i][i]
    for j in range(n):
        if j == i: continue
        if values[i][j] > val: res.append(j)
    return res



# Hardkodede tester på formatet (n, values)
tests = [
    (1, [[1]]),
    (2, [[1, 0], [0, 1]]),
    (2, [[0, 1], [1, 0]]),
    (3, [[1, 2, 2], [0, 1, 2], [0, 2, 1]]),
    (5, [
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]),
    (5, [
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
        [1, 0, 0, 0, 0],
    ]),
    (5, [
        [0, 1, 0, 0, 1],
        [1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0],
        [1, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
    ]),
    (5, [
        [0, 1, 0, 0, 0],
        [0, 0, 1, 0, 0],
        [0, 0, 0, 1, 0],
        [0, 0, 0, 0, 1],
        [1, 0, 0, 0, 0],
    ]),
    (5, [
        [3, 5, 2, 1, 2],
        [1, 4, 5, 3, 3],
        [5, 5, 6, 8, 1],
        [0, 1, 1, 2, 3],
        [8, 3, 5, 6, 7],
    ]),
    (6, [
        [0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0],
    ]),
    (6, [
        [3, 1, 2, 2, 1, 4],
        [6, 7, 9, 5, 1, 6],
        [3, 3, 4, 7, 2, 1],
        [1, 5, 1, 2, 0, 1],
        [3, 3, 6, 2, 4, 3],
        [1, 6, 6, 7, 9, 8],
    ]),
]

def gen_examples(n_l, n_u, k):
    # Tester med liten sannsynlighet for misunnelsessykler
    for _ in range(k//2):
        n = random.randint(n_l, n_u)
        values = [[int(random.randint(0, 9) == 9) for _ in range(n)] for _ in range(n)]
        yield n, values

    # Tester med stor sannsynlighet for misunnelsessykler
    for _ in range(k - k//2):
        n = random.randint(n_l, n_u)
        values = [[random.randint(0, 9) for _ in range(n)] for _ in range(n)]
        yield n, values


def gen_answers(n, values):
    # Sjekker om instans har en misunnelsessykel ved hjelp av bruteforce
    # NB: Veldig tregt for store instanser.
    cycle_exists = False
    agents = list(range(n))
    for k in range(1, n + 1):
        for x in permutations(agents, k):
            if valid_cycle(values, x):
                yield list(x)
                cycle_exists = True
    if not cycle_exists:
        yield None

def valid_cycle(values, answer):
    # Sjekker om answer er en gyldig misunnelsessykel
    return all(values[x][y] > values[x][x] for x, y in zip(answer, answer[1:] +
                                                           answer[:1]))

if generate_random_tests:
    if seed:
        random.seed(seed)
    tests += list(gen_examples(n_lower, n_upper, random_tests))

failed = False
for n, values in tests:
    possible_answers = list(gen_answers(n, values))
    answer = detect_envy_cycle(n, [row[:] for row in values])

    if answer not in possible_answers:
        if failed:
            print("-"*50)
        failed = True
        print(f"""
Koden feilet for følgende instans:
Agenter: {n}
Verdier:
{chr(10).join(', '.join(map(str, row)) for row in values)}

Ditt svar var {answer}, mens mulige svar er:""")
        print(*possible_answers, sep="\n", end="\n\n")

if not failed:
    print("Koden ga riktig svar for alle eksempeltestene")
