from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)

import numpy as np
import scipy.sparse as scpy


class AdjacencyMatrixFA:
    def __init__(self, automaton: NondeterministicFiniteAutomaton = None):
        self.start_states: set[int] = set()
        self.final_states: set[int] = set()
        self.count_states: int = 0
        self.states = {}
        self.adj_matrix = {}

        if automaton is None:
            return

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
