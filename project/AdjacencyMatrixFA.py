from collections import defaultdict
from itertools import product
from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from typing import Iterable, Optional, Any

import scipy.sparse as sp
import numpy as np
from typing_extensions import Self

from project.finite_automaton_utils import regex_to_dfa, graph_to_nfa


class AdjacencyMatrixFA:
    _symbol_matrices: dict[Symbol, sp.csr_matrix]
    _start_states: set[int]
    _final_states: set[int]
    _states_to_int: dict[State, int]

    @staticmethod
    def __enumerate_value(value) -> dict[Any, int]:
        return {val: idx for idx, val in enumerate(value)}

    def __init__(self, nfa: Optional[NondeterministicFiniteAutomaton]):
        self._symbol_matrices = dict()

        if nfa is None:
            self._states_number = 0
            self._start_states = set()
            self._final_states = set()
            return

        self._states_to_int = self.__enumerate_value(nfa.states)
        self._states_number = len(nfa.states)
        self._start_states = set(self._states_to_int[i] for i in nfa.start_states)
        self._final_states = set(self._states_to_int[i] for i in nfa.final_states)

        symbol_to_adj_matrix = defaultdict(
            lambda: np.zeros((self._states_number, self._states_number), dtype=bool)
        )

        for start_state, symbol_to_finish_states in nfa.to_dict().items():
            for symbol, finish_states in symbol_to_finish_states.items():
                finish_states = (
                    {finish_states} if type(finish_states) is State else finish_states
                )
                for finish_state in finish_states:
                    symbol_to_adj_matrix[symbol][
                        self._states_to_int[start_state],
                        self._states_to_int[finish_state],
                    ] = True

        for symbol, adj_matrix in symbol_to_adj_matrix.items():
            self._symbol_matrices[symbol] = sp.csr_matrix(adj_matrix, dtype=bool)

    def __find_path(self, word: Iterable[Symbol]):
        stack = [(list(word), start_state) for start_state in self._start_states]

        while len(stack):
            word, state = stack.pop()

            if not len(word):
                if state in self._final_states:
                    return True
                continue

            symbol = word[0]
            if symbol in self._symbol_matrices.keys():
                for i in range(self._states_number):
                    if self._symbol_matrices[symbol][state, i]:
                        stack.append((word[1:], i))

        return False

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.__find_path(word)

    def transitive_closure(self) -> np.ndarray:
        sum_matrix = sp.csr_matrix(sum(self._symbol_matrices.values())).todense()

        size = sum_matrix.shape[0]
        for k in range(size):
            for i in range(size):
                for j in range(size):
                    sum_matrix[i, j] = sum_matrix[i, j] or (
                        sum_matrix[i, k] and sum_matrix[k, j]
                    )

        return sum_matrix

    def is_empty(self) -> bool:
        if not self._symbol_matrices:
            return True

        transitive_closure_matrix = self.transitive_closure()

        return not any(
            transitive_closure_matrix[st, final]
            for st, final in product(self._start_states, self._final_states)
        )

    @classmethod
    def intersect(cls, automaton1: Self, automaton2: Self):
        instance = cls(None)

        instance._symbol_matrices = {
            sym: sp.csr_matrix(
                sp.kron(
                    automaton1._symbol_matrices[sym], automaton2._symbol_matrices[sym]
                )
            )
            for sym in set(automaton1._symbol_matrices.keys()).intersection(
                automaton2._symbol_matrices.keys()
            )
        }

        instance._states_to_int = {
            State((st1[0], st2[0])): st1[1] * automaton2._states_number + st2[1]
            for st1, st2 in product(
                automaton1._states_to_int.items(), automaton2._states_to_int.items()
            )
        }

        def get_intersect_states(states1, states2):
            return set(
                st1 * automaton2._states_number + st2
                for st1, st2 in product(states1, states2)
            )

        instance._start_states = get_intersect_states(
            automaton1._start_states, automaton2._start_states
        )
        instance._final_states = get_intersect_states(
            automaton1._final_states, automaton2._final_states
        )

        instance._states_number = automaton1._states_number * automaton2._states_number

        return instance

    @property
    def states_number(self):
        return self._states_number

    @property
    def start_states(self):
        return self._start_states

    @property
    def final_states(self):
        return self._final_states

    @property
    def states_to_int(self):
        return self._states_to_int


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    return AdjacencyMatrixFA.intersect(automaton1, automaton2)


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_dfa = regex_to_dfa(regex)
    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    intersection = AdjacencyMatrixFA.intersect(
        AdjacencyMatrixFA(graph_nfa), AdjacencyMatrixFA(regex_dfa)
    )

    closure = intersection.transitive_closure()

    def get_int_from_state(state1: State, state2: State):
        return intersection.states_to_int[State((state1, state2))]

    if intersection.is_empty():
        result = set()
    else:
        result = set(
            graph_states_pair
            for dfa_states_pair in product(
                regex_dfa.start_states, regex_dfa.final_states
            )
            for graph_states_pair in product(
                graph_nfa.start_states, graph_nfa.final_states
            )
            if closure[
                get_int_from_state(graph_states_pair[0], dfa_states_pair[0]),
                get_int_from_state(graph_states_pair[1], dfa_states_pair[1]),
            ]
        )

    if intersection.accepts([]):
        result = result.union(
            set(
                state_pair
                for state_pair in product(
                    graph_nfa.start_states, graph_nfa.final_states
                )
                if state_pair[0] == state_pair[1]
            )
        )

    return result
