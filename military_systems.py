from collections import deque


def breadth_first_search(graph, start, goal):
    queue = deque()
    visited = set()
    queue.append((start, []))  # Store node and its corresponding path

    while queue:
        current_node, path = queue.popleft()
        if current_node == goal:
            return path + [current_node]

        if current_node not in visited:
            visited.add(current_node)
            for neighbor in graph[current_node]:
                queue.append((neighbor, path + [current_node]))

    return None  # No path found


def initiate_conflict(attack_force, defence_force, battleground):
    attacking_power = attack_force.power_dict[battleground.terrain]
    defending_power = defence_force.power_dict[battleground.terrain]





