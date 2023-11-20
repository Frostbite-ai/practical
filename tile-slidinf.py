import numpy as np
import heapq

class PuzzleState:
    """
    Represents a state of the 8-puzzle.
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
    """
    Calculates the Manhattan distance of a state from the goal.
    """
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i, j] != 0:
                x, y = divmod(goal.index(state[i, j]), 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def get_possible_moves(state):
    """
    Returns a list of possible moves from the current state.
    """
    moves = []
    i, j = np.argwhere(state == 0)[0]
    if i > 0: moves.append(("up", i, j))
    if i < 2: moves.append(("down", i, j))
    if j > 0: moves.append(("left", i, j))
    if j < 2: moves.append(("right", i, j))
    return moves

def generate_new_state(state, move):
    """
    Generates a new state by making a move on the current state.
    """
    i, j = np.argwhere(state == 0)[0]
    new_state = np.copy(state)
    if move == "up": new_state[i, j], new_state[i - 1, j] = new_state[i - 1, j], new_state[i, j]
    elif move == "down": new_state[i, j], new_state[i + 1, j] = new_state[i + 1, j], new_state[i, j]
    elif move == "left": new_state[i, j], new_state[i, j - 1] = new_state[i, j - 1], new_state[i, j]
    elif move == "right": new_state[i, j], new_state[i, j + 1] = new_state[i, j + 1], new_state[i, j]
    return new_state

def best_first_search(initial_state, goal_state):
    """
    Performs Best-First Search to find the shortest path to the goal state.
    """
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
                next_state = PuzzleState(new_state, current_state, move, current_state.depth + 1, cost)
                heapq.heappush(open_list, next_state)

    return None

def reconstruct_path(state):
    """
    Reconstructs the path from the start state to the goal state.
    """
    moves = []
    while state.parent is not None:
        moves.append(state.move)
        state = state.parent
    return moves[::-1]

def print_puzzle(state):
    """
    Prints the puzzle state in a readable format.
    """
    print("\n".join([" ".join(map(str, row)) for row in state]))
    print()

# Main function to solve the puzzle
def solve_puzzle(initial, goal):
    """
    Solves the 8-puzzle and prints each step.
    """
    solution = best_first_search(initial, goal)
    if solution:
        print("Solution found in {} steps.".format(len(solution)))
        for move in solution:
            print("Move:", move)
            initial = generate_new_state(initial, move)
            print_puzzle(initial)
    else:
        print("No solution found.")

# Example usage
initial = np.array([[7, 2, 4], [5, 0, 6], [8, 3, 1]])
goal = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 0]])
print("Initial State:")
print_puzzle(initial)
print("Goal State:")
print_puzzle(goal)
solve_puzzle(initial, goal)
