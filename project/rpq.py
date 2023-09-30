from typing import Set, Tuple, List, Dict, Union
from networkx import MultiDiGraph
from pyformlang.finite_automaton import State
from project.utils.bool_decomposition import BoolDecompositionOfFA
from project.utils.finite_automata_construct import graph_to_nfa, regex_to_min_dfa


def rpq_tensors(
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

    regex_automaton_states_count = len(regex_automaton.states)
    result = set()
    for start, final in transitive_closure:
        if (
            State(start) in intersection.start_states
            and State(final) in intersection.final_states
        ):
            result.add(
                (
                    start // regex_automaton_states_count,
                    final // regex_automaton_states_count,
                )
            )

    return result


def rpq_bfs(
    graph: MultiDiGraph,
    start_states: List[int],
    final_states: List[int],
    regex_query: str,
    group_by_start: bool = False,
) -> Union[Dict[int, Set[int]], Set[int]]:
    graph_automaton = graph_to_nfa(graph, start_states, final_states)
    regex_automaton = regex_to_min_dfa(regex_query)
    bool_graph = BoolDecompositionOfFA.from_fa(graph_automaton)
    bool_regex = BoolDecompositionOfFA.from_fa(regex_automaton)

    return bool_graph.reachable_states_bfs(bool_regex, group_by_start)
