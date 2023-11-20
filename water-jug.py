from collections import deque
from heapq import heappush, heappop


def heuristic(state, target):
    jug1_difference = abs(state[0] - target)
    jug2_difference = abs(state[1] - target)
    return min(jug1_difference, jug2_difference)


def is_valid_state(state, a, b):
    return 0 <= state[0] <= a and 0 <= state[1] <= b


def generate_next_states(current, a, b):
    jug1, jug2 = current
    states = []

    # Fill Jug1, Fill Jug2
    states.extend([(a, jug2), (jug1, b)])

    # Empty Jug1, Empty Jug2
    states.extend([(0, jug2), (jug1, 0)])

    # Pour from Jug1 to Jug2, Pour from Jug2 to Jug1
    pour_amount = min(jug1, b - jug2)
    states.append((jug1 - pour_amount, jug2 + pour_amount))

    pour_amount = min(jug2, a - jug1)
    states.append((jug1 + pour_amount, jug2 - pour_amount))

    return [state for state in states if is_valid_state(state, a, b)]


def a_star_search(jug_capacity_a, jug_capacity_b, target_amount):
    start_state = (0, 0)
    visited = set()
    path_map = {}
    g = {start_state: 0}
    f = {start_state: heuristic(start_state, target_amount)}
    priority_queue = [(f[start_state], start_state)]

    while priority_queue:
        current_cost, current_state = heappop(priority_queue)

        if current_state in visited:
            continue

        visited.add(current_state)

        if target_amount in current_state:
            path = deque()
            while current_state in path_map:
                path.appendleft(current_state)
                current_state = path_map[current_state]
            path.appendleft(start_state)
            return path

        for next_state in generate_next_states(
            current_state, jug_capacity_a, jug_capacity_b
        ):
            new_g = g[current_state] + 1

            if next_state not in visited or new_g < g.get(next_state, float("inf")):
                g[next_state] = new_g
                f[next_state] = new_g + heuristic(next_state, target_amount)
                heappush(priority_queue, (f[next_state], next_state))
                path_map[next_state] = current_state

    return None


def run_water_jug_problem():
    jug_capacity_a = int(input("Enter Jug 1 Capacity: "))
    jug_capacity_b = int(input("Enter Jug 2 Capacity: "))
    target_amount = int(input("Enter Target Amount: "))

    path = a_star_search(jug_capacity_a, jug_capacity_b, target_amount)

    if path:
        print("Solution Path:")
        for state in path:
            print(f"Jug 1: {state[0]}, Jug 2: {state[1]}")
        print("Solution found!")
    else:
        print("No solution possible with given jug sizes and target.")


if __name__ == "__main__":
    run_water_jug_problem()
