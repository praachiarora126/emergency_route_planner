import heapq
import math
from collections import deque


def edge_distance(graph, u, v):
    """Get the shortest available road-edge distance in metres."""
    edges = graph.get_edge_data(u, v)

    if not edges:
        return float("inf")

    return min(
        float(data.get("length", 1))
        for data in edges.values()
    )


def path_distance(graph, path):
    """Calculate the total distance of a path in metres."""
    return sum(
        edge_distance(graph, path[i], path[i + 1])
        for i in range(len(path) - 1)
    )


def heuristic(graph, node, goal):
    """Straight-line distance between two intersections."""
    a = graph.nodes[node]
    b = graph.nodes[goal]

    lat1, lon1 = math.radians(a["y"]), math.radians(a["x"])
    lat2, lon2 = math.radians(b["y"]), math.radians(b["x"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    value = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2)
        * math.sin(dlon / 2) ** 2
    )

    return 6371000 * 2 * math.atan2(
        math.sqrt(value),
        math.sqrt(1 - value)
    )


def bfs(graph, start, goal):
    """Breadth-First Search."""
    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == goal:
            return path

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None


def dfs(graph, start, goal):
    """Depth-First Search."""
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        current = path[-1]

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return None


def greedy_best_first(graph, start, goal):
    """Greedy Best-First Search."""
    priority_queue = [
        (heuristic(graph, start, goal), [start])
    ]
    visited = set()

    while priority_queue:
        _, path = heapq.heappop(priority_queue)
        current = path[-1]

        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        for neighbor in graph.neighbors(current):
            if neighbor not in visited:
                heapq.heappush(
                    priority_queue,
                    (
                        heuristic(graph, neighbor, goal),
                        path + [neighbor]
                    )
                )

    return None


def a_star(graph, start, goal):
    """A* Search using road distance and straight-line heuristic."""
    priority_queue = [
        (heuristic(graph, start, goal), 0, start, [start])
    ]

    best_cost = {start: 0}

    while priority_queue:
        _, cost, current, path = heapq.heappop(priority_queue)

        if cost > best_cost.get(current, float("inf")):
            continue

        if current == goal:
            return path

        for neighbor in graph.neighbors(current):
            new_cost = cost + edge_distance(
                graph, current, neighbor
            )

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost

                priority = (
                    new_cost + heuristic(graph, neighbor, goal)
                )

                heapq.heappush(
                    priority_queue,
                    (
                        priority,
                        new_cost,
                        neighbor,
                        path + [neighbor]
                    )
                )

    return None


# Common function to run any selected algorithm
def find_path(graph, start, goal, algorithm):
    algorithms = {
        "bfs": bfs,
        "dfs": dfs,
        "greedy": greedy_best_first,
        "greedy_best_first": greedy_best_first,
        "astar": a_star,
        "a_star": a_star
    }

    selected = algorithms.get(algorithm.lower())

    if selected is None:
        raise ValueError("Invalid algorithm selected")

    return selected(graph, start, goal)