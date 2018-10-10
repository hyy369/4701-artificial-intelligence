"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now).
See Courseworks for detailed instructions.

@author: YH3072 (YOUR UNI)
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped.
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]

    new_state = []
    for row in range(len(state)):
        new_row = []
        for column in range(len(state[row])):
            if row == i1 and column == j1:
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else:
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)


def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions.
    The result should be a list containing (Action, state) tuples.
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))),
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))]
    """

    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable.
    row, col = 0, 0
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == 0:
                row, col = i, j
    if col < len(state) - 1:
        child_states.append(("Left", swap_cells(state, row, col, row, col + 1)))
    if col > 0:
        child_states.append(("Right", swap_cells(state, row, col, row, col - 1)))
    if row < len(state) - 1:
        child_states.append(("Up", swap_cells(state, row, col, row + 1, col)))
    if row > 0:
        child_states.append(("Down", swap_cells(state, row, col, row - 1, col)))
    return child_states


def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise.
    """
    curr_correct = 0
    for row in state:
        for cell in row:
            if cell != curr_correct: return False
            curr_correct += 1
    return True


def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a queue in BFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # Append start state
    fringe.append(state)
    states_expanded += 1
    if len(fringe) > max_fringe: max_fringe = len(fringe)

    # Search while fringe is not empty
    while fringe:
        curr = fringe.pop(0)
        states_expanded += 1
        closed.add(curr)

        if goal_test(curr):
            # If curr is goal state, return solution
            solution = []
            parent = parents[curr]
            while parent[0] != state:
                solution.append(parent[1])
                parent = parents[parent[0]]
            solution.append(parent[1])
            solution.reverse()
            return solution, states_expanded, max_fringe
        else:
            # Otherwise keep expanding
            for child in get_successors(curr):
                if child[1] not in closed:
                    fringe.append(child[1])
                    if len(fringe) > max_fringe: max_fringe = len(fringe)
                    parents[child[1]] = (curr, child[0])
    return None, states_expanded, max_fringe # No solution found


def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a stack in DFS)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # Append start state
    fringe.append(state)
    if len(fringe) > max_fringe: max_fringe = len(fringe)

    # Search while fringe is not empty
    while fringe:
        curr = fringe.pop()
        states_expanded += 1
        closed.add(curr)

        if goal_test(curr):
            # If curr is goal state, return solution
            solution = []
            parent = parents[curr]
            while parent[0] != state:
                solution.append(parent[1])
                parent = parents[parent[0]]
            solution.append(parent[1])
            solution.reverse()
            return solution, states_expanded, max_fringe
        else:
            # Otherwise keep expanding
            for child in get_successors(curr):
                if child[1] not in closed:
                    fringe.append(child[1])
                    if len(fringe) > max_fringe: max_fringe = len(fringe)
                    parents[child[1]] = (curr, child[0])
    return None, states_expanded, max_fringe # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """
    heuristic = 0
    curr_correct = 0
    for row in state:
        for cell in row:
            if cell != curr_correct: heuristic += 1
            curr_correct += 1
    return heuristic


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the Manhattan distance between the current
    position and the goal position. Then return the sum of all distances.
    """
    sum = 0
    for row in range(len(state)):
        for col in range(len(state[row])):
            correct_row = state[row][col] // len(state[row])
            correct_col = state[row][col] % len(state[row])
            sum += abs(correct_row - row) + abs(correct_col - col)
    return sum


def best_first(state, heuristic):
    """
    Best first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}

    # Append start state
    heappush(fringe, (heuristic(state), state))
    states_expanded += 1
    if len(fringe) > max_fringe: max_fringe = len(fringe)

    # Search while fringe is not empty
    while fringe:
        curr = heappop(fringe)[1]
        states_expanded += 1
        closed.add(curr)

        if goal_test(curr):
            # If curr is goal state, return solution
            solution = []
            parent = parents[curr]
            while parent[0] != state:
                solution.append(parent[1])
                parent = parents[parent[0]]
            solution.append(parent[1])
            solution.reverse()
            return solution, states_expanded, max_fringe
        else:
            # Otherwise keep expanding
            for child in get_successors(curr):
                if child[1] not in closed:
                    heappush(fringe, (heuristic(child[1]), child[1]))
                    if len(fringe) > max_fringe: max_fringe = len(fringe)
                    parents[child[1]] = (curr, child[0])

    return None, states_expanded, max_fringe # No solution found


def astar(state, heuristic):
    """
    A-star search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the fringe.
    You may want to keep track of three mutable data structures:
    - The fringe of nodes to expand (operating as a priority queue in greedy search)
    - A set of closed nodes already expanded
    - A mapping (dictionary) from a given node to its parent and associated action
    """
    # You may want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    states_expanded = 0
    max_fringe = 0

    fringe = []
    closed = set()
    parents = {}
    costs = {}

    # Append start state
    costs[state] = 0
    heappush(fringe, (heuristic(state), state))
    states_expanded += 1
    if len(fringe) > max_fringe: max_fringe = len(fringe)

    # Search while fringe is not empty
    while fringe:
        curr = heappop(fringe)[1]
        states_expanded += 1
        closed.add(curr)

        if goal_test(curr):
            # If curr is goal state, return solution
            solution = []
            parent = parents[curr]
            while parent[0] != state:
                solution.append(parent[1])
                parent = parents[parent[0]]
            solution.append(parent[1])
            solution.reverse()
            return solution, states_expanded, max_fringe
        else:
            # Otherwise keep expanding
            for child in get_successors(curr):
                if child[1] not in closed:
                    costs[child[1]] = costs[curr] + 1
                    heappush(fringe, (costs[curr] + 1 + heuristic(child[1]), child[1]))
                    if len(fringe) > max_fringe: max_fringe = len(fringe)
                    parents[child[1]] = (curr, child[0])

    return None, states_expanded, max_fringe # No solution found


def print_result(solution, states_expanded, max_fringe):
    """
    Helper function to format test output.
    """
    if solution is None:
        print("No solution found.")
    else:
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max fringe size: {}.".format(max_fringe))



if __name__ == "__main__":

    #Easy test case
    test_state = ((1, 4, 2),
                  (0, 5, 8),
                  (3, 6, 7))

    #More difficult test case
    test_state = ((7, 2, 4),
                 (5, 0, 6),
                 (8, 3, 1))

    print(state_to_string(test_state))
    print()

    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_fringe = bfs(test_state) #
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))

    # print(get_successors(((0, 4, 2), (1, 5, 8),(3, 6, 7))))
    print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_fringe = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_fringe = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_fringe)
    print("Total time: {0:.3f}s".format(end-start))
