from collections import defaultdict
from itertools import product
from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from typing import Iterable, Optional, Self

import scipy.sparse as sp
import numpy as np

from project.task2 import regex_to_dfa, graph_to_nfa


class AdjacencyMatrixFA:
    __matrix_type: type(sp.spmatrix)
    __symbol_matrices: dict[Symbol, type(sp.spmatrix)]
    __start_states: set[int]
    __final_states: set[int]
    __states_to_int: dict[State, int]
    __states_number: int

    @staticmethod
    def __enumerate_value(value):
        states_to_int = dict()
        int_to_states = dict()
        for idx, val in enumerate(value):
            states_to_int[val] = idx
            int_to_states[idx] = val
        return states_to_int, int_to_states

    def __init__(
        self,
        nfa: Optional[NondeterministicFiniteAutomaton],
        matrix_type: type(sp.spmatrix) = sp.csr_matrix,
    ):
        self.__matrix_type = matrix_type
        self.__symbol_matrices = dict()

        if nfa is None:
            self.__states_number = 0
            self.__start_states = set()
            self.__final_states = set()
            return

        self.__states_to_int, self.__int_to_states = self.__enumerate_value(nfa.states)
        self.__states_number = len(nfa.states)
        self.__start_states = set(self.__states_to_int[i] for i in nfa.start_states)
        self.__final_states = set(self.__states_to_int[i] for i in nfa.final_states)

        self.__symbol_matrices = defaultdict(
            lambda: matrix_type(
                (self.__states_number, self.__states_number), dtype=bool
            )
        )

        for start_state, symbol_to_finish_states in nfa.to_dict().items():
            for symbol, finish_states in symbol_to_finish_states.items():
                finish_states = (
                    {finish_states} if type(finish_states) is State else finish_states
                )
                for finish_state in finish_states:
                    self.__symbol_matrices[symbol][
                        self.__states_to_int[start_state],
                        self.__states_to_int[finish_state],
                    ] = True

    def __find_path(self, word: Iterable[Symbol]):
        stack = [(list(word), start_state) for start_state in self.__start_states]

        while len(stack):
            word, state = stack.pop()

            if not len(word):
                if state in self.__final_states:
                    return True
                continue

            symbol = word[0]
            if symbol in self.__symbol_matrices.keys():
                for i in range(self.__states_number):
                    if self.__symbol_matrices[symbol][state, i]:
                        stack.append((word[1:], i))

        return False

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.__find_path(word)

    def transitive_closure(self) -> np.ndarray:
        sum_matrix = sp.lil_matrix(sum(self.__symbol_matrices.values()))
        sum_matrix.setdiag(True)
        closure = sp.linalg.matrix_power(sum_matrix, self.__states_number)
        return closure

    def is_empty(self) -> bool:
        if not self.__symbol_matrices:
            return True

        transitive_closure_matrix = self.transitive_closure()

        return not any(
            transitive_closure_matrix[st, final]
            for st, final in product(self.__start_states, self.__final_states)
        )

    @classmethod
    def intersect(cls, automaton1: Self, automaton2: Self):
        instance = cls(None)

        instance.__matrix_type = automaton1.matrix_type

        instance.__symbol_matrices = {
            sym: instance.__matrix_type(
                sp.kron(
                    automaton1.symbol_matrices[sym], automaton2.symbol_matrices[sym]
                )
            )
            for sym in set(automaton1.symbol_matrices.keys()).intersection(
                automaton2.symbol_matrices.keys()
            )
        }

        instance.__int_to_states = {}
        instance.__states_to_int = {}
        for st1, st2 in product(
            automaton1.states_to_int.items(), automaton2.states_to_int.items()
        ):
            state = State((st1[0], st2[0]))
            num = st1[1] * automaton2.states_number + st2[1]
            instance.__states_to_int[state] = num
            instance.__int_to_states[num] = state

        def get_intersect_states(states1, states2):
            return set(
                st1 * automaton2.states_number + st2
                for st1, st2 in product(states1, states2)
            )

        instance.__start_states = get_intersect_states(
            automaton1.start_states, automaton2.start_states
        )
        instance.__final_states = get_intersect_states(
            automaton1.final_states, automaton2.final_states
        )

        instance.__states_number = automaton1.states_number * automaton2.states_number

        return instance

    @property
    def states_number(self):
        return self.__states_number

    @property
    def start_states(self):
        return self.__start_states

    @property
    def final_states(self):
        return self.__final_states

    @property
    def states_to_int(self):
        return self.__states_to_int

    @property
    def symbol_matrices(self):
        return self.__symbol_matrices

    @property
    def matrix_type(self):
        return self.__matrix_type

    @property
    def int_to_states(self):
        return self.__int_to_states


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    return AdjacencyMatrixFA.intersect(automaton1, automaton2)


def tensor_based_rpq(
    regex: str,
    graph: MultiDiGraph,
    start_nodes: set[int],
    final_nodes: set[int],
    matrix_type: type(sp.spmatrix) = sp.csr_matrix,
) -> set[tuple[int, int]]:
    regex_dfa = regex_to_dfa(regex)
    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    intersection = AdjacencyMatrixFA.intersect(
        AdjacencyMatrixFA(graph_nfa, matrix_type=matrix_type),
        AdjacencyMatrixFA(regex_dfa, matrix_type=matrix_type),
    )

    closure = intersection.transitive_closure()

    if intersection.is_empty():
        result = set()
    else:
        result = {
            (
                intersection.int_to_states[start].value[0],
                intersection.int_to_states[final].value[0],
            )
            for start, final in zip(*closure.nonzero())
            if start in intersection.start_states and final in intersection.final_states
        }

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
