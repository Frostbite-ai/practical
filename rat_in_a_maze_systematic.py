import tkinter as tk


class RatInMazeGame(tk.Tk):
    def __init__(self, maze):
        super().__init__()
        self.title("Rat in Maze Game")
        self.maze = maze
        self.rows = len(maze)
        self.columns = len(maze[0])
        self.buttons = []

        for row in range(self.rows):
            row_buttons = []
            for col in range(self.columns):
                button = tk.Button(
                    self,
                    text="",
                    width=8,
                    height=4,
                    command=lambda r=row, c=col: self.move(r, c),
                )
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.path = []
        self.start()

    def start(self):
        for row in range(self.rows):
            for col in range(self.columns):
                if self.maze[row][col] == 0:
                    self.buttons[row][col].config(bg="white")
                else:
                    self.buttons[row][col].config(bg="black")

        self.row = 0
        self.col = 0
        self.path = [(self.row, self.col)]
        self.buttons[0][0].config(bg="green")
        self.solve(0, 0)

    def move(self, row, col):
        if self.maze[row][col] == 1:
            return

        self.row = row
        self.col = col
        self.path.append((row, col))
        self.buttons[row][col].config(bg="green")
        self.solve(row, col)

    def solve(self, row, col):
        if row == self.rows - 1 and col == self.columns - 1:
            for r, c in self.path:
                self.buttons[r][c].config(bg="blue")
            return

        # Directions: Down, Right, Up, Left
        directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (
                0 <= new_row < self.rows
                and 0 <= new_col < self.columns
                and self.maze[new_row][new_col] == 0
                and (new_row, new_col) not in self.path
            ):
                self.move(new_row, new_col)


if __name__ == "__main__":
    maze = [
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [1, 0, 0, 1, 0],
    ]
    app = RatInMazeGame(maze)
    app.mainloop()
