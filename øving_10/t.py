# def earliest_arrival(timetable, start, goal):
#     stations = {start: 0}
#     while True:
#         idle = True
#         for u, v, ud, va in timetable:
#             if u in stations and stations[u] <= ud and (v not in stations or stations[v] > va):
#                 stations[v] = va
#                 idle = False
#         if idle : break
#     return stations.get(goal, -1)

import heapq

def earliest_arrival(timetable, start, goal):
    # Opprett en graf som representerer togforbindelser
    graph = {}
    for a, b, t0, t1 in timetable:
        if a not in graph:
            #mulig implementasjon av set
            graph[a] = []
        graph[a].append((b, t0, t1))

    # Opprett en prioritetskø (heap) for å holde stasjoner og ankomsttider
    heap = [(0, start)]

    # Opprett en dictionary for å holde den tidligste ankomsttiden til hver stasjon
    arrival_times = {start: 0}

    while heap:
        time, current_station = heapq.heappop(heap)

        if current_station == goal:
            return time

        if current_station in graph:
            for destination, departure_time, arrival_time in graph[current_station]:
                if destination not in arrival_times or (arrival_time < arrival_times[destination] and departure_time >= time):
                    arrival_times[destination] = arrival_time
                    heapq.heappush(heap, (arrival_time, destination))

    return -1  # Hvis målet ikke kan nås

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