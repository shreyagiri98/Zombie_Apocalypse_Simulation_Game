from heapq import heappush, heappop

def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def get_neighbors(pos, world):
    x, y = pos
    neighbors = []

    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x = x + dx
        new_y = y + dy

        if (0 <= new_x < world.grid_width and 
            0 <= new_y < world.grid_height and
            not world.is_safe_zone(new_x, new_y)):  
            neighbors.append((new_x, new_y))

    return neighbors

def find_path(start, goal, world):
    
    if world.is_safe_zone(*goal):
        return []

    frontier = []
    heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current = heappop(frontier)[1]

        if current == goal:
            break

        for next_pos in get_neighbors(current, world):
            new_cost = cost_so_far[current] + 1

            if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                cost_so_far[next_pos] = new_cost
                priority = new_cost + manhattan_distance(goal, next_pos)
                heappush(frontier, (priority, next_pos))
                came_from[next_pos] = current

    # Reconstruct path
    path = []
    current = goal
    while current != start:
        path.append(current)
        current = came_from.get(current)
        if current is None:  # No path found
            return []
    path.append(start)
    path.reverse()

    return path