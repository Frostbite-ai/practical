import heapq
import math

ROW = 9
COL = 10


def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL


def is_unblocked(grid, row, col):
    return grid[row][col] == 1


def is_destination(row, col, dest):
    return (row, col) == dest


def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) ** 2 + (col - dest[1]) ** 2)


def trace_path(cell_details, dest):
    path = []
    row, col = dest
    while (
        cell_details[row][col]["parent_i"] != row
        or cell_details[row][col]["parent_j"] != col
    ):
        path.append((row, col))
        temp_row = cell_details[row][col]["parent_i"]
        temp_col = cell_details[row][col]["parent_j"]
        row = temp_row
        col = temp_col
    path.append((row, col))
    path.reverse()
    return path


def get_neighbors(cell):
    row, col = cell
    neighbors = []
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if is_valid(new_row, new_col) and is_unblocked(grid, new_row, new_col):
            neighbors.append((new_row, new_col))
    return neighbors


def a_star_search(grid, src, dest):
    open_list = [(0, src)]
    cell_details = {}
    cell_details[src] = {"f": 0, "g": 0, "h": 0, "parent": None}

    while open_list:
        current_f, current_cell = heapq.heappop(open_list)
        if current_cell == dest:
            path = []
            while current_cell:
                path.append(current_cell)
                current_cell = cell_details[current_cell]["parent"]
            return path[::-1]

        for neighbor in get_neighbors(current_cell):
            neighbor_g = cell_details[current_cell]["g"] + 1
            neighbor_h = calculate_h_value(neighbor[0], neighbor[1], dest)
            neighbor_f = neighbor_g + neighbor_h

            if neighbor not in cell_details or neighbor_g < cell_details[neighbor]["g"]:
                cell_details[neighbor] = {
                    "f": neighbor_f,
                    "g": neighbor_g,
                    "h": neighbor_h,
                    "parent": current_cell,
                }
                heapq.heappush(open_list, (neighbor_f, neighbor))

    return None


# Define the grid
grid = [
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1],
]

src = (0, 8)
dest = (0, 0)

path = a_star_search(grid, src, dest)

# Print the grid and the path
for i in range(ROW):
    for j in range(COL):
        if (i, j) == src:
            print("S", end=" ")
        elif (i, j) == dest:
            print("D", end=" ")
        elif (i, j) in path:
            print("*", end=" ")
        elif grid[i][j] == 0:
            print("█", end=" ")
        else:
            print(".", end=" ")
    print()
