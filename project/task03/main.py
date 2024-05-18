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
            self.matrix, self.start, self.final, self.state_map = (
                FiniteAutomaton.__from_nfa(automaton)
            )
            self.int_map = list(automaton.states)
        else:
            self.matrix = automaton
            self.start = set() if start is None else start
            self.final = set() if final is None else final
            self.state_map = dict() if state_map is None else state_map

    def accepts(self, word) -> bool:
        nfa = FiniteAutomaton.__to_nfa(self)
        return nfa.accepts("".join(list(word)))

    def is_empty(self) -> bool:
        nfa = FiniteAutomaton.__to_nfa(self)
        return nfa.is_empty()

    def size(self):
        return len(self.state_map)

    def start_indices(self):
        return {self.state_map[i] for i in self.start}

    def final_indices(self):
        return {self.state_map[i] for i in self.final}

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
                            automaton.state_map[u], label, automaton.state_map[v]
                        )

        for s in automaton.start:
            nfa.add_start_state(automaton.state_map[s])
        for s in automaton.final:
            nfa.add_final_state(automaton.state_map[s])

        return nfa


def intersect_automata(a: FiniteAutomaton, b: FiniteAutomaton) -> FiniteAutomaton:
    labels = {label for label in a.matrix.keys() if label in b.matrix}

    automaton = FiniteAutomaton(
        {label: kron(a.matrix[label], b.matrix[label], "csr") for label in labels}
    )

    for u, i in a.state_map.items():
        for v, j in b.state_map.items():

            k = len(b.state_map) * i + j
            automaton.state_map[k] = k

            if u in a.start and v in b.start:
                automaton.start.add(k)

            if u in a.final and v in b.final:
                automaton.final.add(k)

    return automaton


def transitive_closure(fa: FiniteAutomaton):
    if fa.is_empty():
        return csr_matrix((0, 0), dtype=bool)

    result = sum(fa.matrix.values()) + np.eye(fa.size(), fa.size(), dtype=bool)

    p = 0
    f_sparse = csr_matrix(result)
    while True:
        p_new = f_sparse.count_nonzero()
        if p_new == p:
            break
        p = p_new
        f_sparse += f_sparse @ f_sparse
    return f_sparse


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[NodeView, NodeView]]:
    graph_a = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    constraints_a = FiniteAutomaton(regex_to_dfa(regex))

    intersected = intersect_automata(graph_a, constraints_a)
    tc = transitive_closure(intersected)

    size = constraints_a.size()
    result = set()
    for u, v in zip(*tc.nonzero()):
        if u in intersected.start and v in intersected.final:
            result.add((graph_a.state_map[u // size], graph_a.state_map[v // size]))

    if len(constraints_a.start & constraints_a.final) > 0:
        result |= {(i, i) for i in start_nodes & final_nodes}

    return list(result)
