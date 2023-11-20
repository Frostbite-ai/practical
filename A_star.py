import heapq
import math
import tkinter as tk
import time

ROW = 9
COL = 10

def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid, row, col):
    return grid[row][col] == 1

def is_destination(row, col, dest):
    return (row, col) == dest

def calculate_h_value(row, col, dest):
    return math.sqrt((row - dest[0]) * 2 + (col - dest[1]) * 2)

def trace_path(cell_details, dest):
    path = []
    row, col = dest
    while cell_details[row][col]['parent_i'] != row or cell_details[row][col]['parent_j'] != col:
        path.append((row, col))
        temp_row = cell_details[row][col]['parent_i']
        temp_col = cell_details[row][col]['parent_j']
        row = temp_row
        col = temp_col
    path.append((row, col))
    path.reverse()
    return path

window = tk.Tk()
window.title("A* Pathfinding")
canvas = tk.Canvas(window, width=400, height=400)
canvas.pack()

cell_width = 40
cell_height = 40

grid = [
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
    [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
]

src = (0, 8)
dest = (0, 0)

for i in range(ROW):
    for j in range(COL):
        x1, y1 = j * cell_width, i * cell_height
        x2, y2 = x1 + cell_width, y1 + cell_height
        if grid[i][j] == 0:
            canvas.create_rectangle(x1, y1, x2, y2, fill="black")
        else:
            canvas.create_rectangle(x1, y1, x2, y2, fill="white")

src_point = canvas.create_oval(src[1] * cell_width, src[0] * cell_height, (src[1] + 1) * cell_width, (src[0] + 1) * cell_height, fill="green")
dest_point = canvas.create_oval(dest[1] * cell_width, dest[0] * cell_height, (dest[1] + 1) * cell_width, (dest[0] + 1) * cell_height, fill="red")

def visualize_search(path):
    for i in range(len(path) - 1):
        x1, y1 = path[i][1] * cell_width + cell_width // 2, path[i][0] * cell_height + cell_height // 2
        x2, y2 = path[i + 1][1] * cell_width + cell_width // 2, path[i + 1][0] * cell_height + cell_height // 2
        canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)
        canvas.update()
        time.sleep(0.2)
       
       
       
def get_neighbors(cell):
    row, col = cell
    neighbors = []
    moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dr, dc in moves:
        new_row, new_col = row + dr, col + dc
        if is_valid(new_row, new_col):
            if is_unblocked(grid,new_row, new_col):
                neighbors.append((new_row, new_col))

    return neighbors


def a_star_search(grid, src, dest):
    open_list = [(0, src)]
    cell_details = {}
    cell_details[src] = {'f': 0, 'g': 0, 'h': 0, 'parent': None}
    # f=total cost function(g+h) g=cost to reach curr from starting h=heuristic
    while open_list:
        # Pop the cell with the lowest 'f' value from the open list
        current_f, current_cell = heapq.heappop(open_list)
        if current_cell == dest:
            path = []
            while current_cell:
                path.append(current_cell)
                current_cell = cell_details[current_cell]['parent']
            return path[::-1]  # Reverse the path

        for neighbor in get_neighbors(current_cell):
            # Calculate neighbor's 'g' value
            neighbor_g = cell_details[current_cell]['g'] + 1

            # Calculate neighbor's 'h' value (heuristic)
            neighbor_h = calculate_h_value(neighbor[0], neighbor[1], dest)
            neighbor_f = neighbor_g + neighbor_h

            # Check if neighbor is in the open list or closed list
            if neighbor in cell_details:
                # If neighbor is already in cell_details, check if the new path is better
                if neighbor_g < cell_details[neighbor]['g']:
                    cell_details[neighbor]['g'] = neighbor_g
                    cell_details[neighbor]['h'] = neighbor_h
                    cell_details[neighbor]['f'] = neighbor_f
                    cell_details[neighbor]['parent'] = current_cell
                    heapq.heappush(open_list, (neighbor_f, neighbor))
            else:
                cell_details[neighbor] = {'f': neighbor_f, 'g': neighbor_g, 'h': neighbor_h, 'parent': current_cell}
                heapq.heappush(open_list, (neighbor_f, neighbor))
    # If the open list is empty and destination not reached, return None
    return None


start_button = tk.Button(window, text="Run A* Search", command=lambda: visualize_search(a_star_search(grid, src, dest)))
start_button.pack()
window.mainloop()