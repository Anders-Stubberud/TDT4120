#!/usr/bin/python3
# coding=utf-8
import random


# De lokale testene består av to deler. Et sett med hardkodete
# instanser som kan ses lengre nede, og muligheten for å generere
# tilfeldig instanser. Genereringen av de tilfeldige instansene
# kontrolleres ved å juste på verdiene under.

# Kontrollerer om det genereres tilfeldige instanser.
generate_random_tests = False
# Antall tilfeldige tester som genereres
random_tests = 10
# Lavest mulig antall verdier i generert instans.
n_lower = 3
# Høyest mulig antall verdier i generert instans.
n_upper = 10
# Om denne verdien er 0 vil det genereres nye instanser hver gang.
# Om den er satt til et annet tall vil de samme instansene genereres
# hver gang, om verdiene over ikke endres.
seed = 0
# Kontrollerer om resultatet av tester som feiler skal skrives ut i kompakt
# eller detaljert format.
compact_print = True


def sort(stack1, stack2, stack3):
    while not stack1.empty():
        element = stack1.pop()
        while not stack2.empty() and element > stack2.peek():
            stack3.push(stack2.pop())
        stack2.push(element)
        while not stack3.empty():
            stack2.push(stack3.pop())
    while not stack2.empty():
        stack3.push(stack2.pop())
    while not stack3.empty():
        stack1.push(stack3.pop())


# Hardkodetetester, høyre side blir toppen av stakken
tests = [
    [4, 3, 2, 1],
    [1, 2, 3, 4],
    [4, 2, 1, 7],
    [1, 1, 1, 1],
    [7, 3, 9, 2, 0, 1, 3, 4],
    [7, 3, 0, 13, 48, 49, 233, 9, 2, 0, 1, 3, 4],
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


class Counter:
    def __init__(self):
        self.value = 0

    def increment(self):
        self.value += 1

    def decrement(self):
        self.value -= 1

    def get_value(self):
        return self.value


class Stack:
    def __init__(self, operation_counter, element_counter, initial=None):
        self.stack = []
        if initial is not None:
            self.stack = initial

        self.element_counter = element_counter
        self.operation_counter = operation_counter

    def push(self, value):
        if self.element_counter.get_value() <= 0:
            raise RuntimeError(
                "Du kan ikke ta vare på flere elementer på "
                "stakkene enn det fantes originalt."
            )
        self.stack.append(value)
        self.element_counter.decrement()
        self.operation_counter.increment()

    def pop(self):
        if self.element_counter.get_value() >= 2:
            raise RuntimeError(
                "Du kan ikke ha mer enn 2 elementer i minnet " "av gangen."
            )
        self.element_counter.increment()
        self.operation_counter.increment()
        return self.stack.pop()

    def peek(self):
        self.operation_counter.increment()
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0

failed = False
first = True

for test in tests:
    counter1 = Counter()
    counter2 = Counter()
    stack1 = Stack(counter1, counter2, initial=test[:])
    stack2, stack3 = Stack(counter1, counter2), Stack(counter1, counter2)

    sort(stack1, stack2, stack3)

    result = []
    counter2.value = float("-inf")
    while not stack1.empty():
        result.append(stack1.pop())

    if not first:
        print("-"*50)

    if result != sorted(test) and compact_print:
        print(f"""
Koden feilet for følgende instans:
Start (stack1, fra topp til bunn): {test[::-1]}

Ditt svar (stack1, fra topp til bunn): {result}
Forventet svar: {sorted(test)}
""")
        failed = True
    elif result != sorted(test):
        result2 = []
        while not stack2.empty():
            result2.append(stack2.pop())

        result3 = []
        while not stack3.empty():
            result3.append(stack3.pop())
        print(f"""
Koden feilet for følgende instans.
---------------
 Starttilstand
---------------

--------
Stack 1:
--------
{chr(10).join(map(str, test[::-1])) or "ingen elementer i stakken"}

--------------
 Sluttilstand
--------------

--------
Stack 1:
--------
{chr(10).join(map(str, result)) or "ingen elementer i stakken"}

--------
Stack 2:
--------
{chr(10).join(map(str, result2)) or "ingen elementer i stakken"}

--------
Stack 3:
--------
{chr(10).join(map(str, result3)) or "ingen elementer i stakken"}
""")
        failed = True
    else:
        print(f"""
Koden brukte {counter1.get_value() - len(result)} operasjoner på sortering av
{test[::-1]}
""")

    first = False

if not failed:
    print("Koden din fungerte for alle eksempeltestene.")