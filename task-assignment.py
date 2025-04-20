import itertools

def get_input():
    num_tasks = int(input("Enter the number of tasks: "))
    num_processors = int(input("Enter the number of processors: "))

    print("\nEnter the cost matrix (rows=tasks, columns=processors):")
    cost_matrix = []
    for i in range(num_tasks):
        row = list(map(int, input(f"Cost for Task {i} on all processors: ").split()))
        if len(row) != num_processors:
            raise ValueError("Each row must have the same number of processors.")
        cost_matrix.append(row)

    return num_tasks, num_processors, cost_matrix

def serial_assignment_cost(cost_matrix):
    cost = 0
    for task_index, costs in enumerate(cost_matrix):
        processor = task_index % len(costs)
        cost += costs[processor]
    return cost

def optimal_assignment_cost(cost_matrix):
    num_tasks = len(cost_matrix)
    num_processors = len(cost_matrix[0])
    min_cost = float('inf')
    best_assignment = []

    all_possible_assignments = itertools.product(range(num_processors), repeat=num_tasks)
    for assignment in all_possible_assignments:
        current_cost = sum(cost_matrix[i][assignment[i]] for i in range(num_tasks))
        if current_cost < min_cost:
            min_cost = current_cost
            best_assignment = assignment

    return min_cost, best_assignment

# MAIN
if __name__ == "__main__":
    print("Task Assignment Cost Calculator")
    num_tasks, num_processors, cost_matrix = get_input()

    serial_cost = serial_assignment_cost(cost_matrix)
    print(f"\nSerial Assignment Cost: {serial_cost}")

    if num_tasks <= 10:  # Keep brute-force feasible
        optimal_cost, best_assignment = optimal_assignment_cost(cost_matrix)
        print(f"Optimal Assignment Cost: {optimal_cost}")
        print(f"Best Assignment: {['Task ' + str(i) + ' → P' + str(p) for i, p in enumerate(best_assignment)]}")
    else:
        print("Too many tasks for brute-force optimal calculation. Use heuristic or optimization algorithm.")


# Enter the number of tasks: 3
# Enter the number of processors: 2

# Cost for Task 0 on all processors: 10 5
# Cost for Task 1 on all processors: 6 4
# Cost for Task 2 on all processors: 3 2
