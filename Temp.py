from collections import deque
import math
import heapq

graph = {
    "Atlanta": {"Dallas": 721, "Houston": 702, "Chicago": 588, "Washington": 543, "Miami": 604},
    "Boston": {"Detroit": 613, "New York": 190},
    "Chicago": {"Seattle": 1737, "Riverside": 1704, "Dallas": 805, "Atlanta": 588, "Detroit": 238},
    "Dallas": {"Phoenix": 887, "Chicago": 805, "Houston": 225, "Atlanta": 721},
    "Detroit": {"Chicago": 238, "Boston": 613, "New York": 482, "Washington": 396},
    "Houston": {"Phoenix": 1015, "Dallas": 225, "Atlanta": 702, "Miami": 968},
    "Los Angeles": {"San Francisco": 348, "Riverside": 50, "Phoenix": 357},
    "Miami": {"Houston": 968, "Washington": 923, "Atlanta": 604},
    "New York": {"Detroit": 482, "Boston": 190, "Philadelphia": 81},
    "Philadelphia": {"New York": 81, "Washington": 123},
    "Phoenix": {"Los Angeles": 357, "Riverside": 307, "Dallas": 887, "Houston": 1015},
    "Riverside": {"San Francisco": 386, "Los Angeles": 50, "Phoenix": 307, "Chicago": 1704},
    "San Francisco": {"Seattle": 678, "Los Angeles": 348, "Riverside": 386},
    "Seattle": {"San Francisco": 678, "Chicago": 1737},
    "Washington": {"Detroit": 396, "Philadelphia": 123, "Atlanta": 543, "Miami": 923},
}


M_E_C = min(
    cost 
    for neighbor in graph.values() 
    for cost in neighbor.values()
)


def H_D_T_G (graph, goal):
    distances = {goal : 0}
    queue = deque([goal])

    while queue:
        current = queue.popleft()

        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)

    return distances


def M_Heuristic (graph, goal):
    hop_dt = H_D_T_G (graph, goal)

    def heuristic (city):
        return hop_dt[city] * M_E_C

    return heuristic


def reconstruct_path (parent, start, goal):
    path = [goal]

    while path[-1] != start:
        path.append(parent[path[-1]])

    path.reverse()
    return path


def a_star (graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError (f"Unknown City of {start} or {goal}")
    
    g_score = {city: math.inf for city in graph}
    g_score[start] = 0
    heuristic = M_Heuristic(graph, goal)
    parent = {}
    open_heap = [(heuristic(start), 0, start)]

    while open_heap:
        f_n, g_current, current = heapq.heappop(open_heap)

        if g_current != g_score[current]:
            continue

        if current == goal:
            return reconstruct_path(parent, start, goal), g_score[goal]

        for neighbor, edge_cost in graph[current].items():
            tent_g = g_current + edge_cost

            if tent_g < g_score[neighbor]:
                g_score[neighbor] = tent_g
                parent[neighbor] = current
                heapq.heappush(open_heap, (heuristic(neighbor) + tent_g, tent_g, neighbor))

    raise ValueError ("No Path Exist")


if __name__ == "__main__":
    start, goal = "Detroit", "Miami"
    path, cost = a_star(graph, start, goal)
    print(" -> ".join(path))
    print(f"Total cost: {cost}")