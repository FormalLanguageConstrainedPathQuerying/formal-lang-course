from typing import Set, Hashable, Tuple

from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import *


def rpq(
    regex: Regex,
    graph: MultiDiGraph,
    start_nodes: Set[Hashable] = None,
    final_nodes: Set[Hashable] = None,
) -> set[tuple[Hashable, Hashable]]:
    nfa = build_nfa(graph, start_nodes, final_nodes)
    dfa = build_minimal_dfa(regex)

    intersected_automatas = BoolMatrix(nfa).intersect(BoolMatrix(dfa))
    start_states = intersected_automatas.start_states
    final_states = intersected_automatas.final_states

    closure = intersected_automatas.transitive_closure()

    return {
        (start_state, finish_state)
        for start_state, finish_state in zip(*closure.nonzero())
        if start_state in start_states and finish_state in final_states
    }
