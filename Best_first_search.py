import queue


class BestFirstSearch:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid_values = [[0] * grid_size for _ in range(grid_size)]

    def heuristic(self, row, col, target_row, target_col):
        # Manhattan distance
        return abs(target_row - row) + abs(target_col - col)

    def best_first_search(self, target_row, target_col):
        visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        q = queue.PriorityQueue()
        q.put((0, (0, 0)))  # Starting from the top-left corner
        came_from = {}

        while not q.empty():
            _, (row, col) = q.get()
            print(f"Visiting: ({row}, {col})")
            visited[row][col] = True

            if row == target_row and col == target_col:
                self.reconstruct_path(came_from, target_row, target_col)
                break

            # Getting the neighbors of the current cell
            neighbors = self.get_neighbors(row, col)

            # Adding neighbors to the queue
            for r, c in neighbors:
                if not visited[r][c]:
                    priority = self.heuristic(r, c, target_row, target_col)
                    q.put((priority, (r, c)))
                    came_from[(r, c)] = (row, col)

    def get_neighbors(self, row, col):
        neighbors = []
        if row > 0:
            neighbors.append((row - 1, col))
        if row < self.grid_size - 1:
            neighbors.append((row + 1, col))
        if col > 0:
            neighbors.append((row, col - 1))
        if col < self.grid_size - 1:
            neighbors.append((row, col + 1))
        return neighbors

    def reconstruct_path(self, came_from, target_row, target_col):
        path = []
        current = (target_row, target_col)
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.reverse()
        print("Path to target:", path)


if __name__ == "__main__":
    grid_size = 5
    target_row, target_col = 4, 4  # Example target position
    bfs = BestFirstSearch(grid_size)
    print(
        f"Finding path to target ({target_row}, {target_col}) in a {grid_size}x{grid_size} grid."
    )
    bfs.best_first_search(target_row, target_col)
