def calculate_cost(nodes, operator, base_costs, weight=1):
    """Calculate the cost based on the specified operator (AND/OR)."""
    if operator == "AND":
        return sum(base_costs[node] + weight for node in nodes)
    elif operator == "OR":
        return min(base_costs[node] + weight for node in nodes)

def get_combined_cost(base_costs, conditions, weight=1):
    """Calculate the combined cost for each condition."""
    combined_cost = {}

    for key, value in conditions.items():
        for op in ["AND", "OR"]:
            if op in value:
                nodes = value[op]
                path = f" {op} ".join(nodes)
                cost = calculate_cost(nodes, op, base_costs, weight)
                combined_cost[path] = cost

    return combined_cost

def update_base_costs(base_costs, conditions, weight=1):
    """Update the base costs using the combined cost of each condition."""
    updated_costs = {}
    for condition_key in reversed(conditions.keys()):
        condition = conditions[condition_key]
        combined_cost = get_combined_cost(base_costs, {condition_key: condition}, weight)
        min_cost = min(combined_cost.values())
        base_costs[condition_key] = min_cost
        updated_costs[condition_key] = combined_cost
    return updated_costs

def find_shortest_path(start_node, updated_costs, base_costs):
    """Find the shortest path from the start node using the updated costs."""
    path = start_node
    total_cost = 0

    if start_node in updated_costs:
        min_cost = min(updated_costs[start_node].values())
        for path_key, cost in updated_costs[start_node].items():
            if cost == min_cost:
                total_cost += min_cost
                next_nodes = path_key.split()
                if len(next_nodes) == 1:
                    next_node = next_nodes[0]
                    next_path, next_cost = find_shortest_path(next_node, updated_costs, base_costs)
                    path += " <-- " + next_path
                    total_cost += next_cost
                else:
                    path += " <-- (" + path_key + ") "
                    for next_node in next_nodes:
                        next_path, next_cost = find_shortest_path(next_node, updated_costs, base_costs)
                        path += "[" + next_path + " + "
                        total_cost += next_cost
                    path += "]"
    return path, total_cost

# Example usage
base_costs = {"A": -1, "B": 5, "C": 2, "D": 4, "E": 5, "F": 10, "G": 3, "H": 4, "I": 15, "J": 10}
conditions = {
    "A": {"OR": ["B"], "AND": ["C", "D"]},
    "B": {"AND": ["E", "F"]},
    "C": {"AND": ["G", "H"]},
    "D": {"AND": ["I", "J"]},
}

weight = 1
print("Updated Cost:")
updated_costs = update_base_costs(base_costs, conditions, weight)
print("*" * 75)
final_path, final_cost = find_shortest_path("A", updated_costs, base_costs)
print("Shortest Path:", final_path)
print("Shortest Path Cost:", final_cost)
