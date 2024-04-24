from typing import Any

import numpy as np
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
)
from scipy.sparse import csr_matrix, kron

from project.task02 import graph_to_nfa, regex_to_dfa
from networkx import MultiDiGraph
from networkx.classes.reportviews import NodeView


class FiniteAutomaton:

    def __init__(self, automaton=None, start=None, final=None, state_map=None):

        if isinstance(
            automaton, (DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton)
        ):
            self.matrix, self.istart, self.ifinal, self.istate_map = (
                FiniteAutomaton.__from_nfa(automaton)
            )
        else:
            self.matrix = automaton

            self.istart = set() if start is None else start
            self.ifinal = set() if final is None else final
            self.istate_map = dict() if state_map is None else state_map
        self.start = set() if start is None else start
        self.final = set() if final is None else final
        self.state_map = dict() if state_map is None else state_map

    def accepts(self, word) -> bool:
        nfa = FiniteAutomaton.__to_nfa(self)
        return nfa.accepts("".join(list(word)))

    def is_empty(self) -> bool:
        return len(self.matrix) == 0

    def size(self):
        return len(self.state_map)

    @staticmethod
    def __from_nfa(automaton: NondeterministicFiniteAutomaton) -> tuple:
        n = len(automaton.states)
        states = automaton.to_dict()
        state_map = {v: i for i, v in enumerate(automaton.states)}

        # В старой домашке тесты без этого проходят
        def to_set(a):
            return a if isinstance(a, set) else {a}

        matrix = dict()
        for label in automaton.symbols:
            matrix[label] = csr_matrix((n, n), dtype=bool)
            for u, edges in states.items():
                if label in edges:
                    for v in to_set(edges[label]):
                        matrix[label][state_map[u], state_map[v]] = True

        return matrix, automaton.start_states, automaton.final_states, state_map

    @staticmethod
    def __to_nfa(automaton) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        for label in automaton.matrix.keys():
            m_size = automaton.matrix[label].shape[0]
            for u in range(m_size):
                for v in range(m_size):
                    if automaton.matrix[label][u, v]:
                        nfa.add_transition(
                            automaton.istate_map[u], label, automaton.istate_map[v]
                        )

        for s in automaton.istart:
            nfa.add_start_state(automaton.istate_map[s])
        for s in automaton.ifinal:
            nfa.add_final_state(automaton.istate_map[s])

        return nfa


def intersect_automata(a: FiniteAutomaton, b: FiniteAutomaton) -> FiniteAutomaton:
    labels = {label for label in a.matrix.keys() if label in b.matrix}

    automaton = FiniteAutomaton(
        {label: kron(a.matrix[label], b.matrix[label], "csr") for label in labels}
    )

    for u, i in a.istate_map.items():
        for v, j in b.istate_map.items():

            k = len(b.istate_map) * i + j
            automaton.istate_map[k] = k

            if u in a.istart and v in b.istart:
                automaton.istart.add(k)

            if u in a.ifinal and v in b.ifinal:
                automaton.ifinal.add(k)

    return automaton


def transitive_closure(fa: FiniteAutomaton):
    if fa.is_empty():
        return csr_matrix((0, 0), dtype=bool)

    result = np.zeros_like(next(iter(fa.matrix.values())), dtype=bool)
    for m in fa.matrix.values():
        result += m

    p = 0
    f_sparse = csr_matrix(result)
    while True:
        p_new = f_sparse.count_nonzero()
        if p_new == p:
            break
        p = p_new
        f_sparse = f_sparse @ f_sparse
    return result


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[NodeView, NodeView]]:
    automaton_graph = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    automaton_regex = FiniteAutomaton(regex_to_dfa(regex))
    return reachable_under_constraint(automaton_graph, automaton_regex)


def reachable_under_constraint(
    a: FiniteAutomaton, b: FiniteAutomaton
) -> list[tuple[NodeView, NodeView]]:
    intersected = intersect_automata(a, b)
    tc = transitive_closure(intersected)

    size = b.size()
    result = []
    for u, v in zip(*tc.nonzero()):
        if u in intersected.start and v in intersected.final:
            result.append((a.state_map[u // size], a.state_map[v // size]))
    return result
