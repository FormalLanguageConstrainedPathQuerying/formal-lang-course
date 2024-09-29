from functools import reduce
from itertools import product
from typing import Iterable, cast
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    Symbol,
)
from .graph_utils import graph_to_nfa
from .regex_utils import regex_to_dfa

import numpy.typing as np_type
import numpy as np
import scipy.sparse as scpy
from scipy.sparse.linalg import matrix_power


class AdjacencyMatrixFA:
    def __init__(self, automaton: NondeterministicFiniteAutomaton = None):
        self.start_states = set()
        self.final_states = set()
        self.count_states: int = 0
        self.states = {}
        self.adj_matrix = {}

        if automaton is None:
            return

        graph = automaton.to_networkx()

        self.states = {state_name: i for i, state_name in enumerate(graph.nodes)}
        self.count_states = len(self.states)
        self.start_states = set(st for st in automaton.start_states)
        self.final_states = set(st for st in automaton.final_states)

        self.adj_matrix = {
            sym: scpy.csr_matrix((self.count_states, self.count_states), dtype=bool)
            for sym in automaton.symbols
        }

        for st, end, label in graph.edges(data="label"):
            if not label:
                continue

            self.adj_matrix[label][self.states[st], self.states[end]] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        configs_stack = [
            (list(word), start_state_name) for start_state_name in self.start_states
        ]

        while len(configs_stack) > 0:
            config = configs_stack.pop()
            word = config[0]
            current_state_name = config[1]

            if len(word) == 0:
                if current_state_name in self.final_states:
                    return True
                continue

            matrix = self.adj_matrix.get(word[0], None)
            if matrix is None:
                continue

            current_state_index = self.states[current_state_name]
            for next_state_name, next_state_index in self.states.items():
                if matrix[current_state_index, next_state_index]:
                    configs_stack.append((word[1:], next_state_name))

        return False

    def transitive_closure(self) -> np_type.NDArray[np.bool_]:
        result = np.eye(self.count_states, dtype=bool)

        for adj_matrix in self.adj_matrix.values():
            result = result | adj_matrix.toarray()

        for i in range(2, self.count_states + 1):
            result_after = matrix_power(result, i)
            if np.array_equal(result, result_after):
                return result
            result = result_after

        return result

    def is_empty(self) -> bool:
        transitive_closure = self.transitive_closure()
        for start_state in self.start_states:
            for final_state in self.final_states:
                if transitive_closure[
                    self.states[start_state], self.states[final_state]
                ]:
                    return False

        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    intersect_fa = AdjacencyMatrixFA()

    intersect_fa.adj_matrix = kronecker_product(
        automaton1.adj_matrix, automaton2.adj_matrix
    )
    intersect_fa.count_states = automaton1.count_states * automaton2.count_states
    for st1 in automaton1.states.keys():
        for st2 in automaton2.states.keys():
            new_index = (
                automaton1.states[st1] * automaton2.count_states
                + automaton2.states[st2]
            )
            intersect_fa.states[(st1, st2)] = new_index

            if st1 in automaton1.final_states and st2 in automaton2.final_states:
                intersect_fa.final_states.add((st1, st2))

            if st1 in automaton1.start_states and st2 in automaton2.start_states:
                intersect_fa.start_states.add((st1, st2))

    return intersect_fa


def kronecker_product(adj_matrix1: dict, adj_matrix2: dict) -> dict:
    kron_dict = {}

    for sym in adj_matrix1.keys():
        if sym not in adj_matrix2.keys():
            continue

        matrix1 = adj_matrix1[sym]
        matrix2 = adj_matrix2[sym]
        kron_dict[sym] = cast(
            scpy.csr_matrix, scpy.kron(matrix1, matrix2, format("csr"))
        )

    return kron_dict


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    nfa1 = graph_to_nfa(graph, start_nodes, final_nodes)
    dfa2 = regex_to_dfa(regex)

    graph_AMFA = AdjacencyMatrixFA(nfa1)
    regex_AMFA = AdjacencyMatrixFA(dfa2)

    intersect_fa = intersect_automata(graph_AMFA, regex_AMFA)
    tr_closure = intersect_fa.transitive_closure()

    result = set()

    for start_graph_state, final_graph_state in product(start_nodes, final_nodes):
        for start_regex_state, final_regex_state in product(
            dfa2.start_states, dfa2.final_states
        ):
            start_index = intersect_fa.states[(start_graph_state, start_regex_state)]
            final_index = intersect_fa.states[(final_graph_state, final_regex_state)]
            if tr_closure[start_index, final_index]:
                result.add((start_graph_state, final_graph_state))
    return result
