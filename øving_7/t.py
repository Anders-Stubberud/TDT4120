n = 7

def build_min_heap():
    for i in range(n-1, -1, -1):
        min_heapify(i)
def insert(node):
    global n
    min_queue.append(node)
    current_index = n
    n += 1
    index_parent = current_index // 2 if current_index % 2!= 0 else (current_index // 2) - 1
    print(current_index)
    print(index_parent)
    while index_parent >= 0:
        if min_queue[current_index][1] < min_queue[index_parent][1]:
            min_queue[current_index],  min_queue[index_parent] = min_queue[index_parent], min_queue[current_index]
            current_index = index_parent
            index_parent = index_parent // 2 if index_parent % 2!= 0 else (index_parent // 2) - 1
        else: break
def extract_min():
    minste = min_queue[0]
    min_queue[0] = min_queue.pop()
    global n
    n -= 1
    min_heapify(0)
    return minste
def min_heapify(index):
    verdi = min_queue[index][1]
    venstre = (index * 2) + 1
    if venstre > n - 1: return 
    venstre_verdi = min_queue[venstre][1]
    høyre = (index * 2) + 2
    if høyre <= n - 1:
        høyre_verdi = min_queue[høyre][1]
        if verdi > venstre_verdi or verdi > høyre_verdi:
            if venstre_verdi < høyre_verdi:
                min_queue[index], min_queue[venstre] = min_queue[venstre], min_queue[index]
                min_heapify(venstre)
            else:
                min_queue[index], min_queue[høyre] = min_queue[høyre], min_queue[index]
                min_heapify(høyre)
    else:
        if verdi > venstre_verdi :
            min_queue[index], min_queue[venstre] = min_queue[venstre], min_queue[index]
            min_heapify(venstre)

class Node:
    def __init__(self):
        self.left_child = None
        self.right_child = None

min_queue = [('a', 8), ('a', 1), ('b', 9), ('c', 2), ('a', 11), ('b', 17), ('c', 3)]
build_min_heap()
extract_min()
node = (Node(), 1)
insert(node)
print(min_queue)

