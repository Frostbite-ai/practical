import tkinter as tk
import queue
import math


class BestFirstSearchGUI(tk.Tk):
    def __init__(self, grid_size):
        super().__init__()
        self.title("Best-First Search")
        self.grid_size = grid_size
        self.grid_values = [[0] * grid_size for _ in range(grid_size)]
        self.buttons = []

        for row in range(grid_size):
            row_buttons = []
            for col in range(grid_size):
                button = tk.Button(
                    self,
                    text=str(self.grid_values[row][col]),
                    width=4,
                    height=2,
                    command=lambda r=row, c=col: self.best_first_search(r, c),
                )
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

    def best_first_search(self, target_row, target_col):
        def heuristic(row, col):
            return abs(target_row - row) + abs(target_col - col)  # Manhattan distance

        visited = [[False] * self.grid_size for _ in range(self.grid_size)]
        q = queue.PriorityQueue()
        q.put((0, (0, 0)))
        came_from = {}

        while not q.empty():
            _, (row, col) = q.get()
            self.buttons[row][col].config(bg="green")
            visited[row][col] = True

            if row == target_row and col == target_col:
                self.reconstruct_path(came_from, target_row, target_col)
                break

            neighbors = []
            if row > 0:
                neighbors.append((row - 1, col))
            if row < self.grid_size - 1:
                neighbors.append((row + 1, col))
            if col > 0:
                neighbors.append((row, col - 1))
            if col < self.grid_size - 1:
                neighbors.append((row, col + 1))

            for r, c in neighbors:
                if not visited[r][c]:
                    priority = heuristic(r, c)
                    q.put((priority, (r, c)))
                    came_from[(r, c)] = (row, col)

    def reconstruct_path(self, came_from, target_row, target_col):
        current = (target_row, target_col)
        while current in came_from:
            row, col = current
            self.buttons[row][col].config(bg="blue")
            current = came_from[current]


if __name__ == "__main__":
    grid_size = 5
    app = BestFirstSearchGUI(grid_size)
    app.mainloop()
