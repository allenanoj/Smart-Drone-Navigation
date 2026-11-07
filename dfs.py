
def dfs(grid, start, goal):

    n = len(grid)

    visited = [[False] * n for i in range(n)]
    parent = {}
    order = []
    found = False

    def search(x, y, depth):

        nonlocal found

        visited[x][y] = True
        order.append((x, y))

        # Check destination
        if (x, y) == goal:
            found = True
            return

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

                parent[(nx, ny)] = (x, y)

                search(nx, ny, depth + 1)

                if found:
                    return

    search(start[0], start[1], 0)

    # Reconstruct path
    if not found:
        return None, order

    path = []
    current = goal

    while current != start:
        path.append(current)
        current = parent[current]

    path.append(start)
    path.reverse()

    return path, order