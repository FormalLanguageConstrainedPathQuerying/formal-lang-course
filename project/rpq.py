from project.bool_automaton import *
from project.automata_utils import *


def rpq(graph, regex, start_states=None, final_states=None):
    """
    Calculates which states can be reached by a given regex.

    :param graph: MultiDiGraph
    :param regex: PythonRegex
    :param start_states: set()
    :param final_states: set()
    :return: set() of initial and final state pairs
    """
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
                    i // bool_by_regex.number_of_states,
                    j // bool_by_regex.number_of_states,
                )
            )
    return result
