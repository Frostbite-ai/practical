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
                    width=2,
                    height=1,
                    command=lambda r=row, c=col: self.move(r, c),
                )
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

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
        self.buttons[0][0].config(bg="green")
        self.update()  # Update the GUI to reflect the changes
        self.solve()

    def move(self, row, col):
        if self.maze[row][col] == 1:
            return

        self.buttons[self.row][self.col].config(bg="white")
        self.row = row
        self.col = col
        self.buttons[row][col].config(bg="green")
        self.solve()

    def solve(self):
        if self.row == self.rows - 1 and self.col == self.columns - 1:
            self.buttons[self.row][self.col].config(bg="blue")
            return

        if self.row < self.rows - 1 and self.maze[self.row + 1][self.col] == 0:
            self.move(self.row + 1, self.col)
        elif self.col < self.columns - 1 and self.maze[self.row][self.col + 1] == 0:
            self.move(self.row, self.col + 1)
        else:
            self.buttons[self.row][self.col].config(bg="red")


if __name__ == "__main__":
    maze = [
        [0, 1, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 1, 0, 0],
        [1, 1, 1, 1, 0],
    ]
    app = RatInMazeGame(maze)
    app.mainloop()
