import random
import matplotlib.pyplot as plt

def objective_function(x):
    """
    Objective function to be maximized.
    """
    return -x ** 2 + 10 * x + 20

def hill_climbing(max_iterations, step_size):
    """
    Hill Climbing algorithm: Iteratively explores neighboring nodes and chooses the best one.
    """
    x = random.uniform(0, 10)
    path = [(x, objective_function(x))]  # Store the optimization path

    print(f"Initial position: x = {x}, Value = {objective_function(x)}")

    for i in range(max_iterations):
        current_value = objective_function(x)
        neighbor_x = x + random.uniform(-step_size, step_size)
        neighbor_value = objective_function(neighbor_x)

        print(f"Iteration {i+1}: x = {neighbor_x}, Value = {neighbor_value}")

        if neighbor_value > current_value:
            x = neighbor_x
            path.append((x, neighbor_value))  # Store the new position and value
            print(f"New best found: x = {x}, Value = {neighbor_value}")

    return path

# User input and instructions
print("Hill Climbing Algorithm to maximize the function -x^2 + 10x + 20")
print("Enter the number of iterations and the step size for the algorithm.")

# Collecting user inputs
try:
    max_iterations = int(input("Enter the number of iterations: "))
    step_size = float(input("Enter the step size: "))
except ValueError:
    print("Invalid input. Please enter valid numbers.")
    exit()

# Run the Hill Climbing algorithm
path = hill_climbing(max_iterations, step_size)

# Plotting the path using Matplotlib
x_values, y_values = zip(*path)
plt.plot(x_values, y_values, marker='o', linestyle='-')
plt.xlabel('x')
plt.ylabel('Objective Value')
plt.title('Hill Climbing Optimization Path')
plt.show()
