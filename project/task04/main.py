from project.task03 import FiniteAutomaton, reachable_under_constraint


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:
    result = {s: set() for s in fa.state_map.keys()}
    for k, v in reachable_under_constraint(fa, constraints_fa):
        result[k].add(v)
    return result
