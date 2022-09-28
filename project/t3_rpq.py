from project.t2_finite_automata import *
from project.t3_boolean_matrix_automata import BooleanMatrixAutomata


def rpq(graph, regex, start_states=None, final_states=None):
    bool_matrix_for_graph = BooleanMatrixAutomata(
        build_nfa_from_graph(graph, start_states, final_states)
    )
    bool_matrix_for_regex = BooleanMatrixAutomata(build_minimal_dfa_from_regex(regex))
    intersection = bool_matrix_for_graph.intersect(bool_matrix_for_regex)
    tc = intersection.transitive_closure()
    row, col = tc.nonzero()
    rpq_ans = set()
    for start, fin in zip(row, col):
        if (
            start in intersection.start_state_indexes
            and fin in intersection.final_state_indexes
        ):
            rpq_ans.add(
                (
                    start // bool_matrix_for_regex.number_of_states,
                    fin // bool_matrix_for_regex.number_of_states,
                )
            )
    return rpq_ans
