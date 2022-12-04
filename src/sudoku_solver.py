import itertools

import numpy as np

from src.solver import solver, all_different, composite_successor_generator, group_by

SIZE = 9
BOX_SIZE = 3
A = ord("A")


def sudoku_solver(input):
    # declare all variables
    variables = [(var, domain()) for var in sudoku_variables()]

    # transform the grid into variable names and values
    initial_state = {}
    for col in range(0, SIZE):
        for row in range(0, SIZE):
            val = input[row][col]
            if val == 0:
                continue
            var = var_name(row, col)
            initial_state[var] = val

    # generate the constraints (each column, each row, each box)
    constraints = {}
    for col in range(0, SIZE):
        group = tuple(vars_in_col_i(col))
        constraints[group] = all_different
    for row in range(0, SIZE):
        group = tuple(vars_in_row_i(row))
        constraints[group] = all_different
    for box_y in range(0, SIZE, BOX_SIZE):
        for box_x in range(0, SIZE, BOX_SIZE):
            group = tuple(vars_in_box_i(box_y, box_x))
            constraints[group] = all_different

    successor_generator = successor_generator_observant_of_single_candidate_and_sole_option_cells()

    # use the solver
    solution = solver(variables, constraints, initial_state, successor_generator, update_possible, check_is_goal)

    # convert back to a numpy grid
    if solution is None:
        return np.full((SIZE, SIZE), -1)

    result = np.zeros((SIZE, SIZE), np.ubyte)
    for (var, d) in variables:
        (y, x) = var_coords(var)
        result[y][x] = solution[var].value

    return result


# Game "infrastructure"

def sudoku_variables():
    for col in range(0, SIZE):
        for row in range(0, SIZE):
            yield var_name(row, col)


def domain():
    return [i + 1 for i in range(0, SIZE)]


def var_name(row, col):
    return chr(A + col) + str(row + 1)


def var_coords(var):
    """ (row/y, col/x) for a given variable name """
    return int(var[1]) - 1, ord(var[0]) - A


def box_coords(var):
    (vy, vx) = var_coords(var)
    by = vy - (vy % BOX_SIZE)  # (vy // BOX_SIZE) * BOX_SIZE
    bx = vx - (vx % BOX_SIZE)  # (vx // BOX_SIZE) * BOX_SIZE
    return by, bx


# Group getters

def vars_in_col(var):
    (vy, vx) = var_coords(var)
    return vars_in_col_i(vx)


def vars_in_col_i(col):
    return [var_name(row, col) for row in range(0, SIZE)]


def vars_in_row(var):
    (vy, vx) = var_coords(var)
    return vars_in_row_i(vy)


def vars_in_row_i(row):
    return [var_name(row, col) for col in range(0, SIZE)]


def vars_in_box(var):
    (by, bx) = box_coords(var)
    return vars_in_box_i(by, bx)


def vars_in_box_i(box_y, box_x):
    for y in range(0, BOX_SIZE):
        for x in range(0, BOX_SIZE):
            yield var_name(box_y + y, box_x + x)


# Game logic

def check_is_goal(state):
    return not list(unassigned_variables(state))


def update_possible(state, var, val):
    remove_possible(state, val, *[v for v in itertools.chain(vars_in_col(var), vars_in_row(var), vars_in_box(var))])


def remove_possible(state, val, *vars):
    affected = set([v for v in vars if val in state[v].possible])

    if not affected:
        return

    for var in affected:
        state[var].possible.remove(val)

    # (!) after removing all the possible markings
    for var in affected:
        # check for "line" patterns
        handle_pattern_line(state, var, val)


def handle_pattern_line(state, var, val):
    # if in the box of the target var, there are only two or three vars with the val as possible,
    #  and the xs are all the same, then for the whole row except this box, remove the possibility of the val
    #  or the ys are all the same, then for the whole col except this box, remove the possibility of the val

    box = set(vars_in_box(var))
    potential = [v for v in box if val in state[v].possible]

    n = len(potential)
    if n != 2 and n != 3:
        return

    coords = [var_coords(v) for v in potential]

    # if all are on the same column (same x)
    if len(set([x for (y, x) in coords])) == 1:
        (y, x) = coords[1]
        group = [v for v in vars_in_col_i(x) if v not in box]
        remove_possible(state, val, *group)

    # if all are on the same row (same y)
    if len(set([y for (y, x) in coords])) == 1:
        (y, x) = coords[1]
        group = [v for v in vars_in_row_i(y) if v not in box]
        remove_possible(state, val, *group)


def unassigned_variables(state):
    return [var for var in state.keys() if state[var].value is None]


def successor_generator_basic():
    """
    Very naive implementation that simply
    picks a cell (not even at random)
    and then picks a value for it (not even at random)
    """
    return composite_successor_generator(unassigned_variables, pick_value, update_possible)


def successor_generator_observant_of_single_candidate_and_sole_option_cells():
    return composite_successor_generator(
        pick_single_candidate_or_sole_option_or_unassigned,
        pick_value_closest_to_completion,
        update_possible,
        check_valid
    )


def pick_value(state, var):
    return state[var].possible


def check_valid(state):
    deadends = [var for var, s in state.items() if s.value is None and not s.possible]
    return not deadends


def pick_single_candidate_or_sole_option_or_unassigned(state):
    # find any "Single Candidate" variables, that only have 1 possible value
    single_candidate = [var for var, s in state.items() if len(s.possible) == 1]
    if single_candidate:
        # print("Single Candidates:", single_candidate)
        return [single_candidate[0]]

    # find any "Sole option" variables, that are the only ones with a possibility for a value in their box
    for val in domain():
        potential = set([var for var, s in state.items() if val in s.possible])
        by_box = group_by(potential, box_coords)
        sole_options = [g[0] for box, g in by_box.items() if len(g) == 1]
        if sole_options:
            # print("Sole Options for", val, ":", sole_options)
            return [sole_options[0]]

    # get the unassigned variables that are options for the value closest to completion
    # no need to return all unassigned variables
    # because if the options for even one value lead to no solution, then the state is unsolvable
    freqs = frequencies(state)
    unfinished_values = [v for v in domain() if freqs.get(v, 0) != SIZE]
    value_choices = sorted(unfinished_values, key=lambda val: freqs.get(val, 0), reverse=True)
    target_value = value_choices[0]
    unassigned = [var for var, s in state.items() if s.value is None and target_value in s.possible]

    # print("Unassigned:", unassigned)
    return unassigned


def pick_value_closest_to_completion(state, var):
    possible = state[var].possible

    box = list(vars_in_box(var))
    box.remove(var)
    for val in possible:
        if next((False for other_var in box if val in state[other_var].possible), True):
            # print("Picking value ", val, "for", var, " as no other cell in the box can have it")
            return [val]

    freqs = frequencies(state)

    return sorted(possible, key=lambda val: freqs.get(val, 0), reverse=True)


def frequencies(state):
    freqs = {}
    for s in state.values():
        if s.value is not None:
            freqs[s.value] = freqs.get(s.value, 0) + 1
    return freqs


# debug

def pretty(state):
    res = ""
    for y in range(0, SIZE):
        if y % BOX_SIZE == 0:
            res += "-------------------------------\n"
        for x in range(0, SIZE):
            if x % BOX_SIZE == 0:
                res += "|"
            s = state[var_name(y, x)]
            res += (" " + str(s.value) if s.value is not None else "." + str(len(s.possible))) + " "
        res += "\n"
    return res