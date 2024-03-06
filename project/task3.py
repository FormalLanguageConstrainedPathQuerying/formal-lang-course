import numpy as np
from scipy.sparse import csr_matrix
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    Symbol,
)
from typing import Iterable, Set, List, Tuple
from networkx import MultiDiGraph
import scipy as sp

hasher_vert = {}
hasher_symb = {}


class FiniteAutomaton:
    def __init__(self, automaton=None):
        self.adjacency_matrix = None
        self.adjecency_matrix_bool = None
        self.start_states = set()
        self.final_states = set()
        self.all_states: Set[int] = set()
        self.transitions_map = {}

        if isinstance(
            automaton, (DeterministicFiniteAutomaton, NondeterministicFiniteAutomaton)
        ):
            self.from_pyformlang(automaton)

    def from_pyformlang(
        self, automaton: NondeterministicFiniteAutomaton or DeterministicFiniteAutomaton
    ):
        global hasher_vert, hasher_symb, k_from, k_to, k_symb
        # Convert a pyformlang automaton to the internal representation
        for start_state in automaton.start_states:
            self.start_states.add(start_state.value)

        for final_state in automaton.final_states:
            self.final_states.add(final_state.value)

        self.adjacency_matrix = csr_matrix(
            (len(automaton.states), len(automaton.states)), dtype=str
        )
        self.adjacency_matrix_bool = csr_matrix(
            (len(automaton.states), len(automaton.states)), dtype=bool
        )

        for state in automaton.states:
            self.all_states.add(state.value)

        print(self.all_states)

        transitions = automaton._transition_function._transitions

        k_from = 0
        k_to = 0
        k_symb = 0
        proxy_array = np.zeros((len(automaton.states), len(automaton.states)))
        for fromm in self.all_states:
            if fromm in transitions.keys():
                for symb in transitions[fromm]:
                    to = transitions[fromm][symb]
                    if to not in hasher_vert:
                        hasher_vert[to] = k_to
                        k_to += 1
                    if fromm not in hasher_vert:
                        hasher_vert[fromm] = k_from
                        k_from += 1
                    if symb.value not in hasher_symb:
                        hasher_symb[symb.value] = k_symb
                        k_symb += 1

                    proxy_array[hasher_vert[fromm], hasher_vert[to]] = hasher_symb[
                        symb.value
                    ]
                    self.adjacency_matrix_bool[hasher_vert[fromm], hasher_vert[to]] = (
                        True
                    )

        self.adjacency_matrix = csr_matrix(proxy_array)

    def _accepts(self, state: int, word: Iterable[Symbol]) -> bool:
        if not word:
            if state in self.final_states:
                return True
            return False
        for next_state in self.adjacency_matrix.tocsr()[state].indices:
            next_state = hasher_vert[next_state]
            if (
                self.adjacency_matrix_bool.tocsr()[state, next_state]
                and self.adjacency_matrix.tocsr()[state, next_state] == word[0].value
            ):
                if self._accepts(next_state, word[1:]):
                    return True

        return False

    def accepts(self, word: Iterable[Symbol]) -> bool:
        for start_state in self.start_states:
            if self._accepts(hasher_vert[start_state], word):
                return True

    def is_empty(self) -> bool:
        transitive_closure_matrix = self.adjacency_matrix_bool
        print(transitive_closure_matrix.shape)
        for _ in range(self.adjacency_matrix_bool.shape[0]):
            transitive_closure_matrix = transitive_closure_matrix.dot(
                transitive_closure_matrix
            )

        for i in self.all_states:
            for j in self.all_states:
                if (
                    i in self.start_states
                    and j in self.final_states
                    and transitive_closure_matrix[hasher_vert[i], hasher_vert[j]]
                ):
                    return False

        return True


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    # Intersect two automata and return the resulting automaton
    ans = FiniteAutomaton()
    ans.start_states = automaton1.start_states.intersection(automaton2.start_states)
    ans.final_states = automaton1.final_states.intersection(automaton2.final_states)
    ans.all_states = automaton1.all_states.intersection(automaton2.all_states)

    ans.adjacency_matrix = sp.sparse.kron(
        automaton1.adjacency_matrix, automaton2.adjacency_matrix
    )
    ans.adjacency_matrix_bool = sp.sparse.kron(
        automaton1.adjacency_matrix_bool, automaton2.adjacency_matrix_bool
    )

    return ans


def paths_ends(
    graph: MultiDiGraph, start_nodes: Set[int], final_nodes: Set[int], regex: str
) -> List[Tuple[int, int]]:
    pass
