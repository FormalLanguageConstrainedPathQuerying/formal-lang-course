from functools import reduce
from typing import Iterable
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    Symbol,
)
from graph_utils import graph_to_nfa
from regex_utils import regex_to_dfa

import numpy.typing as np_type
import numpy as np
import scipy.sparse as scpy
from scipy.sparse.linalg import matrix_power


class AdjacencyMatrixFA:
    def __init__(self):
        self.start_states = set()
        self.final_states = set()
        self.count_states: int = 0
        self.states = {}
        self.adj_matrix = {}

    def __init__(self, automaton: NondeterministicFiniteAutomaton):
        graph = automaton.to_networkx()

        self.states = {state_name: i for i, state_name in enumerate(graph.nodes)}
        self.count_states = len(self.states)
        self.start_states = automaton.start_states.copy()
        self.final_states = automaton.final_states.copy()

        self.adj_matrix = {
            sym: scpy.csr_matrix((self.count_states, self.count_states), dtype=bool)
            for sym in automaton.symbols
        }

        for st, end, label in graph.edges(data="label"):
            if not label:
                continue

            self.adj_matrix[label][self.states[st], self.states[end]] = True

    # def accepts(self, word: Iterable[Symbol]) -> bool:
    #     configs_stack = [(list(word), start_state_name) for start_state_name in self.start_states]

    #     while len(configs_stack) > 0:
    #         config = configs_stack.pop()
    #         word = config[0]
    #         current_state_name = config[1]

    #         if len(word) == 0:
    #             if current_state_name in self.final_states:
    #                 return True
    #             continue

    #         adj_row = self.adj_matrix.get(word[0], None)
    #         if adj_row is None:
    #             continue

    #         for applicant_next_state in self.states.values():
    #             if adj_row[current_state_name, applicant_next_state]:
    #                 configs_stack.append((word[1:], applicant_next_state))

    #     return False

    def accepts(self, word: Iterable[Symbol]) -> bool:
        final_states = [self.states(x) for x in self.final_states]
        start_states = [self.states(x) for x in self.start_states]

        def helper(state: int, current_input: list[Symbol]) -> bool:
            if len(current_input) == 0:
                return state in final_states
            sym = current_input[0]
            matrix = self.adj_matrix[sym]
            if not matrix:
                return False

            flag = False
            for next_state in matrix.getrow(state).indices:
                flag = flag or helper(next_state, current_input[1:])
            return flag

        return reduce(
            lambda x, y: x or y, list(map(lambda x: helper(x, word), start_states))
        )

    def transitive_closure(self) -> np_type.NDArray[np.bool_]:
        E_matrix = np.eye(self.count_states, dtype=bool)
        result = E_matrix

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
                    return True

        return False


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    intersect_fa = AdjacencyMatrixFA()

    intersect_fa.adj_matrix = kronecker_product(
        automaton1.adj_matrix, automaton2.adj_matrix
    )
    intersect_fa.start_states = automaton1.start_states | automaton2.start_states
    intersect_fa.final_states = set(
        tuple(qf_1, qf_2)
        for qf_1 in automaton1.final_states
        for qf_2 in automaton2.final_states
    )
    intersect_fa.states = {
        tuple(st1, st2): i * automaton1.count_states + j
        for i, st1 in enumerate(automaton1.states)
        for j, st2 in enumerate(automaton2.states)
    }
    intersect_fa.count_states = len(intersect_fa.states)

    if intersect_fa.count_states != automaton1.count_states * automaton2.count_states:
        raise ValueError("Wrong number of states in the intersection automaton")

    return intersect_fa


def kronecker_product(adj_matrix1: dict, adj_matrix2: dict) -> dict:
    if adj_matrix1.keys() != adj_matrix2.keys():
        raise ValueError("diff alphabet two bool decomposition matrix")
    kron_dict = {}

    for sym in adj_matrix1.keys():
        matrix1 = adj_matrix1[sym]
        matrix2 = adj_matrix2[sym]
        kron_dict[sym] = scpy.kron(matrix1, matrix2)

    return kron_dict


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    nfa1 = graph_to_nfa(graph, start_nodes, final_nodes)
    dfa2 = regex_to_dfa(regex)

    adj_matrix1 = AdjacencyMatrixFA(nfa1)
    adj_matrix2 = AdjacencyMatrixFA(dfa2)

    intersect_fa = intersect_automata(adj_matrix1, adj_matrix2)
    tr_closure = intersect_fa.transitive_closure()

    result = set()

    for start_state in intersect_fa.start_states:
        for final_state in intersect_fa.final_states:
            if tr_closure[
                intersect_fa.states[start_state], intersect_fa.states[final_state]
            ]:
                number_start_state = (
                    intersect_fa.states[start_state] // adj_matrix1.count_states
                )
                number_final_state = (
                    intersect_fa.states[final_state] // adj_matrix1.count_states
                )

                result.add(tuple(number_start_state, number_final_state))

    return result
