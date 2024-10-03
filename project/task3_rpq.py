from functools import reduce
from typing import Iterable
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol
from scipy.sparse import csr_matrix

import numpy as np


class AdjacencyMatrixFA:
    def __init__(self, fa: NondeterministicFiniteAutomaton):
        graph = fa.to_networkx()

        self.states = {st: i for i, st in fa.states}
        self.start_states = {self.states[st] for st in fa.start_states}
        self.final_states = {self.states[st] for st in fa.final_states}
        self.number_of_states = len(self.states)

        transitions = {}
        for symbol in fa.symbols:
            transitions[symbol] = np.zeros(
                (self.number_of_states, self.number_of_states)
            )

        for u, v, label in graph.edges(data="label"):
            if label:
                transitions[label][self.states[u], self.states[v]] = 1

        self.adj_decomposition = {}
        for label, matrix in transitions.items():
            self.adj_decomposition[label] = csr_matrix(matrix)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        symbols = list(word)
        configs = [(st, symbols) for st in self.start_states]

        while configs:
            state, rest = configs.pop()

            if len(rest) == 0 & state in self.final_states:
                return True

            first_symb, *rest_symb = rest

        for next_state in self.states.values():
            if self.adj_decomposition[first_symb][state, next_state]:
                configs.append((next_state, rest_symb))

        return False

    def transitive_closure(self):
        init = csr_matrix((self.number_of_states, self.number_of_states), dtype=bool)
        init.setdiag(True)

        if not self.adj_decomposition:
            return init

        reach: csr_matrix = init + reduce(
            lambda x, y: x + y, self.adj_decomposition.values()
        )

        for k in range(self.number_of_states):
            for i in range(self.number_of_states):
                for j in range(self.number_of_states):
                    reach[i, j] = reach[i, j] or (reach[i, k] and reach[k, j])

        return reach

    def is_empty(self) -> bool:
        tc = self.transitive_closure()
        for start in self.start_states:
            for final in self.final_states:
                if tc[self.states[start], self.states[final]]:
                    return False

        return True
