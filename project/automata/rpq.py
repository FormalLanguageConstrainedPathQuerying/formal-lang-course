from typing import Set, Hashable, Tuple

from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.automata.bool_matrix import BoolMatrix
from project.automata.builders import *


def rpq(
    regex: Regex,
    graph: MultiDiGraph,
    start_nodes: set[Hashable] = None,
    final_nodes: set[Hashable] = None,
) -> set[tuple[Hashable, Hashable]]:
    nfa = build_nfa(graph, start_nodes, final_nodes)
    dfa = build_minimal_dfa(regex)

    nfa_bm = BoolMatrix(nfa)
    dfa_bm = BoolMatrix(dfa)

    intersected_automatas = nfa_bm.intersect(dfa_bm)
    start_states = intersected_automatas.start_states
    final_states = intersected_automatas.final_states

    closure = intersected_automatas.transitive_closure()

    index_to_states = {i: name for name, i in intersected_automatas.states.items()}

    return {
        (index_to_states[start_state][0], index_to_states[finish_state][0])
        for start_state, finish_state in zip(*closure.nonzero())
        if index_to_states[start_state][0] in nfa.start_states
        and index_to_states[finish_state][0] in nfa.final_states
    }
