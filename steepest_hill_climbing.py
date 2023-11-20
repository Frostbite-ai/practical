import random
import matplotlib.pyplot as plt

def objective_function(x):
    """
    Objective function to be maximized.
    """
    return -(x**2)

def hill_climbing(max_iterations, step_size, initial_solution):
    """
    Hill Climbing algorithm: Iteratively explores neighboring nodes and chooses the best one.
    """
    current_solution = initial_solution
    current_value = objective_function(current_solution)
    path = [(current_solution, current_value)]  # Storing path for visualization

    for i in range(max_iterations):
        neighbor_solution = current_solution + random.uniform(-step_size, step_size)
        neighbor_value = objective_function(neighbor_solution)
        path.append((neighbor_solution, neighbor_value))  # Storing each step

        if neighbor_value > current_value:
            current_solution = neighbor_solution
            current_value = neighbor_value

    return current_solution, current_value, path

def plot_path(path):
    """
    Plot the path taken by the hill climbing algorithm.
    """
    x, y = zip(*path)
    plt.plot(x, y, marker='o')
    plt.title('Progression of Hill Climbing Algorithm')
    plt.xlabel('Solution')
    plt.ylabel('Objective Function Value')
    plt.show()

# User input and instructions
print("Hill Climbing Algorithm to maximize the function -(x^2)")
print("You will be asked to enter the number of iterations, step size, and initial solution.")
print("Number of iterations: Total steps the algorithm will take.")
print("Step size: Maximum change allowed in each step.")
print("Initial solution: Starting point of the algorithm.")

# Collecting user inputs
try:
    max_iterations = int(input("Enter the number of iterations: "))
    step_size = float(input("Enter the step size: "))
    initial_solution = float(input("Enter the initial solution: "))
except ValueError:
    print("Invalid input. Please enter valid numbers.")
    exit()

# Run the Hill Climbing algorithm
best_solution, best_value, path = hill_climbing(max_iterations, step_size, initial_solution)

# Print the result and plot the path
print("\nBest Solution:", best_solution)
print("Best Value:", best_value)
plot_path(path)
