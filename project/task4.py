from project import FiniteAutomaton
from scipy.sparse import dok_matrix, block_diag


def reachability_with_constraints(
    finite_automaton: FiniteAutomaton, constraints_automaton: FiniteAutomaton
) -> dict[int, set[int]]:
    matrices = {}

    common_labels = (
        finite_automaton.func_to_steps.keys()
        & constraints_automaton.func_to_steps.keys()
    )
    constraints_height, automaton_height = len(constraints_automaton.map_index_to_state), len(
        finite_automaton.map_index_to_state
    )

    for label in common_labels:
        constraints_matrix = constraints_automaton.func_to_steps[label]
        automaton_matrix = finite_automaton.func_to_steps[label]
        matrices[label] = block_diag((constraints_matrix, automaton_matrix))

    height = constraints_height
    width = constraints_height + automaton_height

    reachable_states = {state.value: set() for state in finite_automaton.map_index_to_state}

    def diagonalize_matrix(matrix):
        height = matrix.shape[0]
        result = dok_matrix(matrix.shape, dtype=bool)

        for i in range(height):
            for j in range(height):
                if matrix[j, i]:
                    result[i] += matrix[j]

        return result

    for start_state in finite_automaton.start_states:
        frontier = dok_matrix((height, width), dtype=bool)
        for constraints_start_state in constraints_automaton.start_states:
            frontier[constraints_start_state, constraints_start_state] = True

        for i in range(height):
            frontier[i, start_state + constraints_height] = True

        for _ in range(constraints_height * automaton_height):
            new_frontier = dok_matrix((height, width), dtype=bool)
            for label in common_labels:
                new_frontier += diagonalize_matrix(frontier @ matrices[label])
            frontier = new_frontier
            for i in range(height):
                if i in constraints_automaton.final_states and frontier[i, i]:
                    for j in range(automaton_height):
                        if (
                            j in finite_automaton.final_states
                            and frontier[i, j + constraints_height]
                        ):
                            reachable_states[
                                finite_automaton.map_index_to_state[start_state]
                            ].add(finite_automaton.map_index_to_state[j])

    return reachable_states
