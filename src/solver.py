from collections import OrderedDict
from copy import deepcopy


def solver(variables, constraints, initial_state, generate_successors, update_possible, check_is_goal):
    state = init_state(variables, initial_state, update_possible)
    return solve(state, constraints, generate_successors, check_is_goal)


def solve(state, constraints, generate_successors, check_is_goal):
    for successor in generate_successors(state):
        # if successor is state: constraints_pass = True  # Hacky memory optimization knowing some choices are "safe"
        if check_constraints(successor, constraints):
            if check_is_goal(successor):
                return successor
            solution = solve(successor, constraints, generate_successors, check_is_goal)
            if solution is not None:
                return solution
    return None


def init_state(variables, initial_state, update_possible):
    state = OrderedDict()

    # start with all possible
    for (var, domain) in variables:
        s = VariableState()
        s.possible = domain
        state[var] = s

    # assign the initial values and update possible values
    for var, val in initial_state.items():
        s = state[var]
        s.value = val
        s.possible = []
        update_possible(state, var, val)

    return state


def check_constraints(state, constraints):
    for variables, constraint in constraints.items():
        values = [state[var].value for var in variables]
        if not constraint(*values):
            return False
    return True


def apply_value(state, var, val):
    s = state[var]
    s.value = val
    s.possible = []


# Common helper functions

def all_different(*args):
    used = set()
    for a in args:
        if a is None:
            continue
        if a in used:
            return False
        used.add(a)
    return True


def composite_successor_generator(pick_variable, pick_value, update_possible, check_valid=lambda s: True):
    """
    A simple successor generator function that used the provided functions
    to pick a variable to update, then pick the value for it, and applies it to produce a successor.
    """

    def generator(state):
        for var in pick_variable(state):
            for val in pick_value(state, var):
                successor = deepcopy(state)
                apply_value(successor, var, val)
                update_possible(successor, var, val)

                if check_valid(successor):
                    yield successor

    return generator


def group_by(items, key_extractor):
    result = OrderedDict()
    for item in items:
        k = key_extractor(item)
        if k in result:
            result[k].append(item)
        else:
            result[k] = [item]
    return result


# State data class

class VariableState:
    value = None
    possible = []

    def __str__(self):
        return "S(" + str(self.value) + " / " + str(self.possible) + ")"

    def __repr__(self):
        return self.__str__()
