from collections import deque


def breadth_first_search(map,
                         graph,
                         start,
                         goal,
                         terrain_routing):
    queue = deque()
    visited = set()
    queue.append((start, []))  # Store node and its corresponding path

    while queue:
        current_node, path = queue.popleft()
        if terrain_routing == 'LAND' and map[current_node].terrain == 'OCEANIC':
            continue
        elif terrain_routing == 'SEA' and map[current_node].terrain == 'CONTINENTAL':
            continue
        if current_node == goal:
            return path + [current_node]
        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph[current_node]:
                queue.append((neighbor, path + [current_node]))

    return None  # No path found






