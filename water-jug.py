import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
from heapq import heappush, heappop


class WaterJugGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Water Jug Problem")

        # Variables
        self.jug1_var = tk.StringVar()
        self.jug2_var = tk.StringVar()
        self.target_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Enter details and start!")

        # Input section
        ttk.Label(root, text="Jug 1 Size:").grid(row=0, column=0, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.jug1_var).grid(
            row=0, column=1, padx=10, pady=5
        )

        ttk.Label(root, text="Jug 2 Size:").grid(row=1, column=0, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.jug2_var).grid(
            row=1, column=1, padx=10, pady=5
        )

        ttk.Label(root, text="Target Amount:").grid(row=2, column=0, padx=10, pady=5)
        ttk.Entry(root, textvariable=self.target_var).grid(
            row=2, column=1, padx=10, pady=5
        )

        ttk.Button(root, text="Start", command=self.start_bfs).grid(
            row=3, column=0, columnspan=2, pady=10
        )

        # Visual representation of jugs
        self.jug1_canvas = tk.Canvas(root, width=100, height=200, bg="white")
        self.jug1_canvas.grid(row=0, rowspan=4, column=2, padx=10)
        self.jug1_fill = self.jug1_canvas.create_rectangle(
            10, 190, 90, 190, fill="blue"
        )

        self.jug2_canvas = tk.Canvas(root, width=100, height=200, bg="white")
        self.jug2_canvas.grid(row=0, rowspan=4, column=3, padx=10)
        self.jug2_fill = self.jug2_canvas.create_rectangle(
            10, 190, 90, 190, fill="blue"
        )

        # Output section
        self.steps_display = ttk.Treeview(root)
        self.steps_display["columns"] = ("Jug 1", "Jug 2")
        self.steps_display.column("#0", width=0, stretch=tk.NO)
        self.steps_display.column("Jug 1", anchor=tk.W, width=80)
        self.steps_display.column("Jug 2", anchor=tk.W, width=80)

        self.steps_display.heading("#0", text="", anchor=tk.W)
        self.steps_display.heading("Jug 1", text="Jug 1", anchor=tk.W)
        self.steps_display.heading("Jug 2", text="Jug 2", anchor=tk.W)

        self.steps_display.grid(row=4, column=0, columnspan=4, padx=10, pady=10)

        ttk.Label(root, textvariable=self.status_var).grid(
            row=5, column=0, columnspan=4, pady=10
        )

        # Control section
        ttk.Button(root, text="Next Step", command=self.show_next_step).grid(
            row=6, column=0, columnspan=2, pady=10
        )
        ttk.Button(root, text="Reset", command=self.reset).grid(
            row=6, column=2, columnspan=2, pady=10
        )

        self.queue = deque()

    def show_next_step(self):
        if self.queue:
            state = self.queue.popleft()
            jug1, jug2 = state
            self.update_jug_display(jug1, jug2)
            self.steps_display.insert("", "end", values=(jug1, jug2))

            if jug1 == int(self.target_var.get()) or jug2 == int(self.target_var.get()):
                self.status_var.set("Solution found!")
                self.queue.clear()
        else:
            self.status_var.set("No more steps!")

    def start_bfs(self):
        try:
            jug1_size = int(self.jug1_var.get())
            jug2_size = int(self.jug2_var.get())
            target = int(self.target_var.get())

            if jug1_size < 0 or jug2_size < 0 or target < 0:
                raise ValueError("Please enter positive numbers.")
            if target > jug1_size and target > jug2_size:
                raise ValueError("Target amount cannot be larger than both jugs.")

            self.status_var.set("Searching...")
            self.steps_display.delete(*self.steps_display.get_children())
            self.queue = a_star_search(jug1_size, jug2_size, target)
            self.show_next_step()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def reset(self):
        self.jug1_var.set("")
        self.jug2_var.set("")
        self.target_var.set("")
        self.status_var.set("Enter details and start!")
        self.steps_display.delete(*self.steps_display.get_children())
        self.queue.clear()
        self.update_jug_display(0, 0)

    def update_jug_display(self, jug1_amount, jug2_amount):
        try:
            jug1_max = int(self.jug1_var.get())
            jug2_max = int(self.jug2_var.get())

            jug1_height = (jug1_amount / jug1_max) * 180
            jug2_height = (jug2_amount / jug2_max) * 180

            self.jug1_canvas.coords(self.jug1_fill, 10, 190 - jug1_height, 90, 190)
            self.jug2_canvas.coords(self.jug2_fill, 10, 190 - jug2_height, 90, 190)

        except ValueError:
            pass


def heuristic(state, target):
    jug1_difference = abs(state[0] - target)
    jug2_difference = abs(state[1] - target)
    return min(jug1_difference, jug2_difference)


def is_valid_state(state, a, b):
    return 0 <= state[0] <= a and 0 <= state[1] <= b


def generate_next_states(current, a, b):
    jug1, jug2 = current
    states = []

    pour_amount = min(jug1, b - jug2)
    states.append((jug1 - pour_amount, jug2 + pour_amount))

    pour_amount = min(jug2, a - jug1)
    states.append((jug1 + pour_amount, jug2 - pour_amount))

    states.extend([(a, jug2), (jug1, b)])
    states.extend([(0, jug2), (jug1, 0)])

    return [state for state in states if is_valid_state(state, a, b)]


def a_star_search(jug_capacity_a, jug_capacity_b, target_amount):
    start_state = (0, 0)
    visited = set()
    path_map = {}
    g = {start_state: 0}
    f = {start_state: heuristic(start_state, target_amount)}
    priority_queue = [(f[start_state], start_state)]
    result = deque()

    while priority_queue:
        current_cost, current_state = heappop(priority_queue)

        if current_state in visited:
            continue

        visited.add(current_state)

        if target_amount in current_state:
            while current_state in path_map:
                result.appendleft(current_state)
                current_state = path_map[current_state]
            result.appendleft(start_state)
            return result

        for next_state in generate_next_states(
            current_state, jug_capacity_a, jug_capacity_b
        ):
            new_g = g[current_state] + 1

            if next_state not in visited or new_g < g.get(next_state, float("inf")):
                g[next_state] = new_g
                f[next_state] = new_g + heuristic(next_state, target_amount)
                heappush(priority_queue, (f[next_state], next_state))
                path_map[next_state] = current_state

    return result


if __name__ == "__main__":
    root = tk.Tk()
    app = WaterJugGUI(root)
    root.mainloop()
