from collections import deque
import heapq
import math

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

MIN_EDGE_COST = min(cost for neighbors in graph.values() for cost in neighbors.values())

def hop_distance_to_goal(graph, goal):
    distances = {goal: 0}
    queue = deque([goal])
    while queue:
        current = queue.popleft()
        for neighbor in graph[current]:
            if neighbor not in distances:
                distances[neighbor] = distances[current] + 1
                queue.append(neighbor)
    return distances

def make_heuristic(graph, goal):
    hop_distances = hop_distance_to_goal(graph, goal)
    def heuristic(city):
        return hop_distances[city] * MIN_EDGE_COST
    return heuristic

def reconstruct_path(parent, start, goal):
    path = [goal]
    while path[-1] != start:
        path.append(parent[path[-1]])
    path.reverse()
    return path

def a_star(graph, start, goal):
    if start not in graph or goal not in graph:
        raise ValueError("Unknown start or goal city")
    heuristic = make_heuristic(graph, goal)
    g_score = {city: math.inf for city in graph}
    g_score[start] = 0
    parent = {}
    open_heap = [(heuristic(start), 0, start)]
    while open_heap:
        _, current_g, current = heapq.heappop(open_heap)
        if current_g != g_score[current]:
            continue
        if current == goal:
            return reconstruct_path(parent, start, goal), g_score[goal]
        for neighbor, edge_cost in graph[current].items():
            tentative_g = current_g + edge_cost
            if tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                parent[neighbor] = current
                heapq.heappush(open_heap, (tentative_g + heuristic(neighbor), tentative_g, neighbor))
    raise ValueError("No path exists")

if __name__ == "__main__":
    start, goal = "Seattle", "Miami"
    path, cost = a_star(graph, start, goal)
    print(" -> ".join(path))
    print(f"Total cost: {cost}")
