
import heapq

def astar(grid, start, goal):
    n = len(grid)

    def heuristic(x, y):
        return abs(x - goal[0]) + abs(y - goal[1])

    q = []
    heapq.heappush(q, (heuristic(start[0], start[1]), 0, start))

    visited = set()
    parent = {}
    cost = {start: 0}
    explored = []

    while q:
        f, g, current = heapq.heappop(q)

        if current in visited:
            continue

        visited.add(current)
        explored.append(current)

        if current == goal:
            break

        x, y = current

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dx, dy in directions:
            nx = x + dx
            ny = y + dy

            if (0 <= nx < n and 0 <= ny < n
                and grid[nx][ny] == 0):

                neighbor = (nx, ny)
                new_cost = g + 1

                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    parent[neighbor] = current

                    f = new_cost + heuristic(nx, ny)
                    heapq.heappush(q, (f, new_cost, neighbor))

    if goal not in visited:
        return None, explored

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path, explored