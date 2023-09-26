from typing import Set, Tuple
from networkx import MultiDiGraph
from project.utils.bool_decomposition import BoolDecompositionOfFA
from project.utils.finite_automata_construct import *


def regular_path_query(
    graph: MultiDiGraph,
    start_states: List[int],
    final_states: List[int],
    regex_query: str,
) -> Set[Tuple[int, int]]:
    graph_automaton = graph_to_nfa(graph, start_states, final_states)
    regex_automaton = regex_to_min_dfa(regex_query)
    bool_graph = BoolDecompositionOfFA.from_fa(graph_automaton)
    bool_regex = BoolDecompositionOfFA.from_fa(regex_automaton)

    intersection = BoolDecompositionOfFA.intersection(bool_graph, bool_regex)
    transitive_closure = BoolDecompositionOfFA.transitive_closure(intersection)

    regex_automata_states_count = len(regex_automaton.states)
    result = set()
    for start, final, label in transitive_closure.edges(data="label"):
        result.add(
            (start // regex_automata_states_count, final // regex_automata_states_count)
        )

    return result
