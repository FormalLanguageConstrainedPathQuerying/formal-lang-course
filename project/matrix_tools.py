from typing import List, Set, Dict, Union, Any

import numpy as np
import scipy.sparse as sps
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol, State

__all__ = ["Adjacency", "BooleanAdjacencies"]


class Adjacency:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None) -> None:
        self.states_num = 0
        self.states_nums = dict()
        self.nums_states = dict()
        self.start_states = set()
        self.final_states = set()

        self.adjacency = list(list(set()))

        if nfa is not None:
            self.states_num = len(nfa.states)
            self.states_nums = {state: num for num, state in enumerate(nfa.states)}
            self.nums_states = {num: state for num, state in enumerate(nfa.states)}
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states

            transition_func = nfa.to_dict()
            self.adjacency = self._get_adjacency(transition_func)

    def _get_adjacency(self, transition_func: Dict[State, Dict[Symbol, Union[State, Set[State]]]]) -> \
            List[List[Set[Symbol]]]:
        adjacency: List[List[Set[Symbol]]] = [[set() for _ in range(self.states_num)] for _ in range(self.states_num)]

        for state_from, transitions in transition_func.items():
            for symbol, states_to in transitions.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}

                for state_to in states_to:
                    state_from_num = self.states_nums[state_from]
                    state_to_num = self.states_nums[state_to]

                    adjacency[state_from_num][state_to_num].add(symbol)

        return adjacency


class BooleanAdjacencies(Adjacency):
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None) -> None:
        super().__init__(nfa)

        self.boolean_adjacencies = dict()

        if nfa is not None:
            symbols = nfa.symbols
            self.boolean_adjacencies = self._get_boolean_adjacencies(symbols)

    def _get_boolean_adjacencies(self, symbols: Set[Symbol]) -> Dict[Symbol, Any]:
        boolean_adjacencies = dict()

        for symbol in symbols:
            boolean_adjacency = np.zeros((self.states_num, self.states_num), dtype=bool)

            for i in range(len(self.adjacency)):
                for j in range(len(self.adjacency[i])):
                    boolean_adjacency[i][j] = symbol in self.adjacency[i][j]

            boolean_adjacencies[symbol] = boolean_adjacency

        return boolean_adjacencies

    def intersect(self, other):
        intersection = BooleanAdjacencies()

        intersection.states_num = self.states_num * other.states_num
        intersection_symbols = self.boolean_adjacencies.keys() & other.boolean_adjacencies.keys()

        for symbol in intersection_symbols:
            intersection.boolean_adjacencies[symbol] = sps.kron(
                sps.csr_matrix(self.boolean_adjacencies[symbol], dtype=bool),
                sps.csr_matrix(other.boolean_adjacencies[symbol], dtype=bool),
                format="csr")

        for graph_state, graph_state_num in self.states_nums.items():
            for query_state, query_state_num in other.states_nums.items():
                intersection_state = State(str(query_state) + '⋂' + str(graph_state))
                intersection_state_num = graph_state_num * other.states_num + query_state_num

                intersection.states_nums[intersection_state] = intersection_state_num
                intersection.nums_states[intersection_state_num] = intersection_state

                if graph_state in self.start_states and query_state in other.start_states:
                    intersection.start_states.add(intersection_state)

                if graph_state in self.final_states and query_state in other.final_states:
                    intersection.final_states.add(intersection_state)

        return intersection

    def get_transitive_closure(self) -> sps.csr_matrix:
        transitive_closure: sps.csr_matrix = sum(
            sps.csr_matrix(boolean_adjacency, dtype=bool) for boolean_adjacency in self.boolean_adjacencies.values())

        current_nnz = transitive_closure.nnz
        new_nnz = 0

        while current_nnz != new_nnz:
            transitive_closure += transitive_closure @ transitive_closure

            current_nnz, new_nnz = new_nnz, transitive_closure.nnz

        return transitive_closure

    def to_nfa(self) -> NondeterministicFiniteAutomaton:
        nfa = NondeterministicFiniteAutomaton()

        for symbol, boolean_adjacency in self.boolean_adjacencies.items():
            for state_from_num, state_to_num in zip(*sps.csr_matrix(boolean_adjacency, dtype=bool).nonzero()):
                state_from = self.nums_states[state_from_num]
                state_to = self.nums_states[state_to_num]

                nfa.add_transition(state_from, symbol, state_to)

        for start_state in self.start_states:
            nfa.add_start_state(start_state)

        for final_state in self.final_states:
            nfa.add_final_state(final_state)

        return nfa
