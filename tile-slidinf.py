import numpy as np
import heapq
import numpy as np
import tkinter as tk
import time


class PuzzleState:
    """
    Represents a state of the 8-puzzle.

    Attributes:
    - state (numpy array): The current state of the puzzle.
    - parent (PuzzleState): The parent state from which this state was reached.
    - move (str): The move made to reach this state from the parent.
    - depth (int): The depth of this state in the search tree.
    - cost (int): The total cost from the start state to this state.
    """

    def __init__(self, state, parent, move, depth, cost):
        self.state = state
        self.parent = parent
        self.move = move
        self.depth = depth
        self.cost = cost

    def __eq__(self, other):
        return np.array_equal(self.state, other.state)

    def __lt__(self, other):
        return self.cost < other.cost


def manhattan_distance(state, goal):
    """Calculates the Manhattan distance of a state from the goal."""
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] != 0:
                x, y = divmod(goal.index(state[i, j]), 3)
                distance += abs(x - i) + abs(y - j)
    return distance


def get_possible_moves(state):
    """Returns a list of possible moves from the current state."""
    moves = []
    i, j = np.argwhere(state == 0)[0]
    if i > 0:
        moves.append(("up", i, j))
    if i < 2:
        moves.append(("down", i, j))
    if j > 0:
        moves.append(("left", i, j))
    if j < 2:
        moves.append(("right", i, j))
    return moves


def generate_new_state(state, move):
    """Generates a new state by making a move on the current state."""
    i, j = np.argwhere(state == 0)[0]
    new_state = np.copy(state)
    if move == "up":
        new_state[i, j], new_state[i - 1, j] = new_state[i - 1, j], new_state[i, j]
    elif move == "down":
        new_state[i, j], new_state[i + 1, j] = new_state[i + 1, j], new_state[i, j]
    elif move == "left":
        new_state[i, j], new_state[i, j - 1] = new_state[i, j - 1], new_state[i, j]
    elif move == "right":
        new_state[i, j], new_state[i, j + 1] = new_state[i, j + 1], new_state[i, j]
    return new_state


def best_first_search(initial_state, goal_state):
    """Performs Best-First Search to find the shortest path to the goal state."""
    goal = goal_state.flatten().tolist()
    open_list = []
    closed_list = set()
    initial_cost = manhattan_distance(initial_state, goal)
    initial_state = PuzzleState(initial_state, None, None, 0, initial_cost)
    heapq.heappush(open_list, initial_state)

    while open_list:
        current_state = heapq.heappop(open_list)
        closed_list.add(tuple(current_state.state.flatten()))

        if np.array_equal(current_state.state, goal_state):
            return reconstruct_path(current_state)

        for move, i, j in get_possible_moves(current_state.state):
            new_state = generate_new_state(current_state.state, move)
            if tuple(new_state.flatten()) not in closed_list:
                cost = manhattan_distance(new_state, goal) + current_state.depth + 1
                next_state = PuzzleState(
                    new_state, current_state, move, current_state.depth + 1, cost
                )
                heapq.heappush(open_list, next_state)

    return None


def reconstruct_path(state):
    """Reconstructs the path from the start state to the goal state."""
    moves = []
    while state.parent is not None:
        moves.append(state.move)
        state = state.parent
    return moves[::-1]


class PuzzleGUI:
    """
    Graphical User Interface for the 8-puzzle solver.

    Attributes:
    - root (tk.Tk): The main window of the application.
    - initial_state (numpy array): The initial state of the puzzle.
    - goal_state (numpy array): The goal state of the puzzle.
    - solution (list): The list of moves to solve the puzzle.
    - current_state (numpy array): The current state of the puzzle during solving.
    - tiles (dict): Dictionary of buttons representing the tiles.
    """


class PuzzleGUI:
    def __init__(self, root, initial_state, goal_state, solution):
        self.root = root
        self.initial_state = initial_state
        self.goal_state = goal_state
        self.solution = solution
        self.current_state = np.copy(initial_state)
        self.tiles = {}

        self.init_ui()

    def init_ui(self):
        self.root.title("8 Puzzle Solver")

        # Frame for the initial state
        initial_frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        initial_frame.grid(row=0, column=0, padx=10, pady=10)

        tk.Label(initial_frame, text="Initial State").grid(
            row=0, columnspan=3
        )  # Using grid instead of pack
        for i in range(3):
            for j in range(3):
                tile = tk.Button(
                    initial_frame, text=str(self.initial_state[i, j]), width=5, height=2
                )
                tile.grid(
                    row=i + 1, column=j
                )  # Adjusted row index to account for the label
                self.tiles[(i, j)] = tile

        # Frame for the goal state
        goal_frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        goal_frame.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(goal_frame, text="Goal State").grid(row=0, columnspan=3)  # Using grid
        for i in range(3):
            for j in range(3):
                tile = tk.Button(
                    goal_frame,
                    text=str(self.goal_state[i, j]),
                    width=5,
                    height=2,
                    state="disabled",
                )
                tile.grid(row=i + 1, column=j)  # Adjusted row index

        # Start button
        start_button = tk.Button(self.root, text="Start", command=self.start_solving)
        start_button.grid(row=1, column=0, columnspan=2)

    def start_solving(self):
        for move in self.solution:
            self.update_state(move)
            self.root.update()
            time.sleep(0.5)  # Delay of 0.5 seconds between moves

    def update_state(self, move):
        i, j = np.argwhere(self.current_state == 0)[0]

        if move == "up":
            self.current_state[i, j], self.current_state[i - 1, j] = (
                self.current_state[i - 1, j],
                self.current_state[i, j],
            )
        elif move == "down":
            self.current_state[i, j], self.current_state[i + 1, j] = (
                self.current_state[i + 1, j],
                self.current_state[i, j],
            )
        elif move == "left":
            self.current_state[i, j], self.current_state[i, j - 1] = (
                self.current_state[i, j - 1],
                self.current_state[i, j],
            )
        elif move == "right":
            self.current_state[i, j], self.current_state[i, j + 1] = (
                self.current_state[i, j + 1],
                self.current_state[i, j],
            )

        self.refresh_tiles()

    def refresh_tiles(self):
        for i in range(3):
            for j in range(3):
                self.tiles[(i, j)]["text"] = str(self.current_state[i, j])


if __name__ == "__main__":
    initial = np.array([[7, 2, 4], [5, 0, 6], [8, 3, 1]])
    goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
    solution = best_first_search(initial, goal)
    root = tk.Tk()
    app = PuzzleGUI(root, initial, goal, solution)
    root.mainloop()
