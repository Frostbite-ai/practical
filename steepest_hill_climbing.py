import random


def objective_function(x):
    return -(x**2)  # curve to maximize


# Hill Climbing algorithm (steepest): explore all neighboring nodes and choose the best one which is nearest to goal
def hill_climbing(max_iterations, step_size, initial_solution):
    current_solution = initial_solution
    current_value = objective_function(current_solution)

    for _ in range(max_iterations):
        # Generate a neighbor solution
        neighbor_solution = current_solution + random.uniform(-step_size, step_size)
        neighbor_value = objective_function(neighbor_solution)

        # If the neighbor solution is better, move to it
        if neighbor_value > current_value:
            current_solution = neighbor_solution
            current_value = neighbor_value

    return current_solution, current_value


# User input for parameters
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
print("Best Solution:", best_solution)
print("Best Value:", best_value)
