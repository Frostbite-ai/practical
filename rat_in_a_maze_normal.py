class RatInMazeGame:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.columns = len(maze[0])
        self.visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]

    def print_maze(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.visited[row][col]:
                    print("R", end=" ")  # 'R' represents the rat's path
                elif self.maze[row][col] == 0:
                    print(".", end=" ")  # '.' represents an open path
                else:
                    print("#", end=" ")  # '#' represents a blocked path
            print()
        print()

    def is_safe(self, row, col):
        return (
            0 <= row < self.rows
            and 0 <= col < self.columns
            and self.maze[row][col] == 0
        )

    def solve(self, row, col):
        if row == self.rows - 1 and col == self.columns - 1:
            self.visited[row][col] = True
            return True

        if self.is_safe(row, col):
            self.visited[row][col] = True

            # Move down
            if self.solve(row + 1, col):
                return True

            # Move right
            if self.solve(row, col + 1):
                return True

            # Backtrack: Unmark this cell as part of the solution path
            self.visited[row][col] = False

        return False


if __name__ == "__main__":
    maze = [
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
    ]
    game = RatInMazeGame(maze)
    game.print_maze()
    if game.solve(0, 0):
        print("Maze solved! Here's the path:")
        game.print_maze()
    else:
        print("No solution found.")
