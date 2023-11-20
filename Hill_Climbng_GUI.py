#hill climbing

import tkinter as tk
# import pygame
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize Pygame
# pygame.init()



def objective_function(x):
    return -x ** 2 + 10 * x + 20


# Hill climbing function
def hill_climbing(max_iterations, step_size):
    x = random.uniform(0, 10)
    path = [(x, objective_function(x))]  # Store the optimization path

    for _ in range(max_iterations):
        current_value = objective_function(x)
        neighbor_x = x + random.uniform(-step_size, step_size)
        neighbor_value = objective_function(neighbor_x)

        if neighbor_value > current_value:
            x = neighbor_x
            path.append((x, neighbor_value))  # Store the new position and value

    return path


# Function to start the optimization
def start_optimization():
    max_iterations = int(iterations_entry.get())
    step_size = float(step_size_entry.get())

    path = hill_climbing(max_iterations, step_size)

    # Plot the optimization path using Matplotlib
    fig, ax = plt.subplots()
    x_values, y_values = zip(*path)
    ax.plot(x_values, y_values, marker='o', linestyle='-')
    ax.set_xlabel('x')
    ax.set_ylabel('Objective Value')
    ax.set_title('Hill Climbing Optimization Path')

    # Embed the Matplotlib plot in Tkinter using FigureCanvasTkAgg
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack()


# Create the main Tkinter window
root = tk.Tk()
root.title("Hill Climbing Optimization with Matplotlib")

# Label and entry for maximum iterations
iterations_label = tk.Label(root, text="Max Iterations:")
iterations_label.pack()
iterations_entry = tk.Entry(root)
iterations_entry.pack()
iterations_entry.insert(0, "100")

# Label and entry for step size
step_size_label = tk.Label(root, text="Step Size:")
step_size_label.pack()
step_size_entry = tk.Entry(root)
step_size_entry.pack()
step_size_entry.insert(0, "0.1")

# Button to start optimization
start_button = tk.Button(root, text="Start Optimization", command=start_optimization)
start_button.pack()

# Run the Tkinter main loop
root.mainloop()