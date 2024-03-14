from project.task3 import FiniteAutomaton, intersect_automata, transitive_closure


def reachability_with_constraints(
    fa: FiniteAutomaton, constraints_fa: FiniteAutomaton
) -> dict[int, set[int]]:

    intersection = intersect_automata(fa, constraints_fa)
    res = {state: set() for state in fa.start_states}

    if intersection.is_empty():
        return res

    from_states, to_states = transitive_closure(intersection).nonzero()
    n = len(constraints_fa.states_map)

    for from_state, to_state in zip(from_states, to_states):
        if (
            from_state in intersection.start_states
            and to_state in intersection.final_states
        ):
            res[fa.states_map[(from_state // n)]].add(fa.states_map[(to_state // n)])

    return res
