
from collections import deque

def bfs(grid, start, goal):

    n = len(grid)

    q = [start]
    visited = [[False] * n for i in range(n)]
    visited[start[0]][start[1]] = True

    parent = {}
    explored = []

    while q:
        x, y = q.pop(0)
        explored.append((x, y))

        if (x, y) == goal:
            break

        # Up, Down, Left, Right
        directions = [
            (-1, 0), (1, 0),
            (0, -1), (0, 1)
        ]

        for dx, dy in directions:

            nx = x + dx
            ny = y + dy

            if (0 <= nx < n and 0 <= ny < n
                and grid[nx][ny] == 0
                and not visited[nx][ny]):

                visited[nx][ny] = True
                parent[(nx, ny)] = (x, y)
                q.append((nx, ny))

    # Reconstruct path
    if not visited[goal[0]][goal[1]]:
        return None, explored

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path, explored
