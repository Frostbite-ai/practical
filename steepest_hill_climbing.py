import random

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
    print(f"Initial Solution: {current_solution}, Value: {current_value}")

    for i in range(max_iterations):
        # Generate a neighbor solution
        neighbor_solution = current_solution + random.uniform(-step_size, step_size)
        neighbor_value = objective_function(neighbor_solution)

        # Show progress
        print(f"Iteration {i+1}: Neighbor Solution: {neighbor_solution}, Value: {neighbor_value}")

        # If the neighbor solution is better, move to it
        if neighbor_value > current_value:
            current_solution = neighbor_solution
            current_value = neighbor_value
            print(f"New Best Found: Solution: {current_solution}, Value: {current_value}")

    return current_solution, current_value

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
best_solution, best_value = hill_climbing(max_iterations, step_size, initial_solution)

# Print the result
print("\nBest Solution:", best_solution)
print("Best Value:", best_value)
