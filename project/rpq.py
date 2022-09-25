from project.bool_automaton import *
from project.automata_utils import *


def rpq(graph, regex, start_states=None, final_states=None):
    bool_by_graph = BoolAutomaton(
        create_nfa_by_graph(graph, start_nodes=start_states, final_nodes=final_states)
    )
    bool_by_regex = BoolAutomaton(create_min_dfa_by_regex(regex))
    bool_intersection = bool_by_graph.intersect(bool_by_regex)
    tc = bool_intersection.transitive_closure()
    x, y = tc.nonzero()
    result = set()
    for i, j in zip(x, y):
        if i in bool_intersection.start_states and j in bool_intersection.final_states:
            result.add(
                (
                    bool_by_graph.get_state_by_number(
                        i // bool_by_regex.number_of_states
                    ),
                    bool_by_graph.get_state_by_number(
                        j // bool_by_regex.number_of_states
                    ),
                )
            )
    return result
