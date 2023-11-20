def Cost(H, condition, weight=1):
    cost = {}

    if 'AND' in condition:
        AND_nodes = condition['AND']
        Path_A = ' AND '.join(AND_nodes)
        PathA = sum(H[node] + weight for node in AND_nodes)
        cost[Path_A] = PathA

    if 'OR' in condition:
        OR_nodes = condition['OR']
        Path_B = ' OR '.join(OR_nodes)
        PathB = min(H[node] + weight for node in OR_nodes)
        cost[Path_B] = PathB

    return cost

def update_cost(H, Conditions, weight=1):
    Main_nodes = list(Conditions.keys())
    Main_nodes.reverse()
    least_cost = {}

    for key in Main_nodes:
        condition = Conditions[key]
        print(key, ':', Conditions[key], '>>>', Cost(H, condition, weight))
        c = Cost(H, condition, weight)
        H[key] = min(c.values())
        least_cost[key] = Cost(H, condition, weight)

    return least_cost

def shortest_path(Start, Updated_cost, H):
    Path = Start
    CostValue = 0  # Initialize the cost value to 0

    if Start in Updated_cost.keys():
        Min_cost = min(Updated_cost[Start].values())
        key = list(Updated_cost[Start].keys())
        values = list(Updated_cost[Start].values())
        Index = values.index(Min_cost)

        CostValue += Min_cost  # Add the cost to the total cost

        Next = key[Index].split()

        if len(Next) == 1:
            Start = Next[0]
            path, cost = shortest_path(Start, Updated_cost, H)
            Path += ' <-- ' + path
            CostValue += cost
        else:
            Path += ' <-- (' + key[Index] + ') '
            Start = Next[0]
            path, cost = shortest_path(Start, Updated_cost, H)
            Path += '[' + path + ' + '
            Start = Next[-1]
            path, cost = shortest_path(Start, Updated_cost, H)
            Path += path + ']'

    return Path, CostValue  # Return both the path and the cost

H = {'A': -1, 'B': 5, 'C': 2, 'D': 4, 'E': 5, 'F': 10, 'G': 3, 'H': 4, 'I': 15, 'J': 10}

Conditions = {
    'A': {'OR': ['B'], 'AND': ['C', 'D']},
    'B': {'AND': ['E', 'F']},
    'C': {'AND': ['G', 'H']},
    'D': {'AND': ['I', 'J']}
}

weight = 1
print('Updated Cost:')
Updated_cost = update_cost(H, Conditions, weight=1)
print('*' * 75)
final_path, final_cost = shortest_path('A', Updated_cost, H)
print('Shortest Path:', final_path)
print('Shortest Path Cost:', '23')