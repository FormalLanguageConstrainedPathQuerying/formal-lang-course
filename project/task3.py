from typing import Iterable

import scipy.sparse as sp
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    Symbol,
)

from project.task2 import graph_to_nfa, regex_to_dfa


class AdjacencyMatrixFA:
    """Finite automaton represented as a sparse boolean adjacency matrix."""

    def __init__(self, automaton: NondeterministicFiniteAutomaton | None = None):
        self._states_count = 0
        self._state_to_index = {}
        self._index_to_state = []
        self._start_states = set()
        self._final_states = set()
        self._bool_matrices = {}
        if automaton is not None:
            self._init_from_automaton(automaton)

    @classmethod
    def from_components(
        cls,
        states_count: int,
        bool_matrices: dict[Symbol, sp.csr_matrix],
        start_states: set[int],
        final_states: set[int],
    ) -> "AdjacencyMatrixFA":
        """Build an automaton from sparse boolean matrices and state sets."""
        fa = cls()
        fa._states_count = states_count
        fa._bool_matrices = bool_matrices
        fa._start_states = start_states
        fa._final_states = final_states
        return fa

    @property
    def states_count(self) -> int:
        return self._states_count

    @property
    def start_states(self) -> set[int]:
        return self._start_states

    @property
    def final_states(self) -> set[int]:
        return self._final_states

    @property
    def bool_matrices(self) -> dict[Symbol, sp.csr_matrix]:
        return self._bool_matrices

    @property
    def index_to_state(self) -> list[State]:
        return self._index_to_state

    def _init_from_automaton(self, automaton: NondeterministicFiniteAutomaton):
        states = set(automaton.states)
        states.update(automaton.start_states)
        states.update(automaton.final_states)

        self._index_to_state = list(states)
        self._state_to_index = {
            state: index for index, state in enumerate(self._index_to_state)
        }
        self._states_count = len(states)

        self._start_states = {self._state_to_index[s] for s in automaton.start_states}
        self._final_states = {self._state_to_index[s] for s in automaton.final_states}

        matrices = {}
        for state_from, transitions in automaton.to_dict().items():
            index_from = self._state_to_index[state_from]
            for symbol, state_tos in transitions.items():
                if isinstance(state_tos, State):
                    state_tos = {state_tos}
                matrix = matrices.setdefault(
                    symbol,
                    sp.lil_matrix((self._states_count, self._states_count), dtype=bool),
                )
                for state_to in state_tos:
                    matrix[index_from, self._state_to_index[state_to]] = True

        self._bool_matrices = {
            symbol: matrix.tocsr() for symbol, matrix in matrices.items()
        }

    def accepts(self, word: Iterable[Symbol]) -> bool:
        """Return ``True`` if the automaton accepts the given word."""
        current = sp.lil_matrix((1, self._states_count), dtype=bool)
        for index in self._start_states:
            current[0, index] = True
        current = current.tocsr()

        for symbol in word:
            symbol = symbol if isinstance(symbol, Symbol) else Symbol(symbol)
            matrix = self._bool_matrices.get(symbol)
            if matrix is None:
                return False
            current = current @ matrix

        return any(current[0, index] for index in self._final_states)

    def _reachability_matrix(self) -> sp.csr_matrix:
        """Reflexive transitive closure of the adjacency matrix."""
        adjacency = sp.csr_matrix((self._states_count, self._states_count), dtype=bool)
        for matrix in self._bool_matrices.values():
            adjacency = adjacency + matrix

        reach = sp.identity(self._states_count, dtype=bool, format="csr") + adjacency
        while True:
            new_reach = (reach + reach @ adjacency).astype(bool)
            if (new_reach != reach).nnz == 0:
                break
            reach = new_reach

        return reach

    def is_empty(self) -> bool:
        """Return ``True`` if the language of the automaton is empty."""
        reach = self._reachability_matrix()
        return not any(
            reach[start, final]
            for start in self._start_states
            for final in self._final_states
        )


def intersect_automata(
    automaton1: AdjacencyMatrixFA,
    automaton2: AdjacencyMatrixFA,
) -> AdjacencyMatrixFA:
    """Return the intersection of two automata built via the tensor product."""
    states_count1 = automaton1.states_count
    states_count2 = automaton2.states_count

    common_symbols = set(automaton1.bool_matrices) & set(automaton2.bool_matrices)

    bool_matrices = {
        symbol: sp.kron(
            automaton1.bool_matrices[symbol],
            automaton2.bool_matrices[symbol],
            format="csr",
        )
        for symbol in common_symbols
    }

    start_states = {
        start1 * states_count2 + start2
        for start1 in automaton1.start_states
        for start2 in automaton2.start_states
    }

    final_states = {
        final1 * states_count2 + final2
        for final1 in automaton1.final_states
        for final2 in automaton2.final_states
    }

    return AdjacencyMatrixFA.from_components(
        states_count1 * states_count2,
        bool_matrices,
        start_states,
        final_states,
    )


def tensor_based_rpq(
    regex: str,
    graph: MultiDiGraph,
    start_nodes: set[int],
    final_nodes: set[int],
) -> set[tuple[int, int]]:
    """Return pairs of start/final nodes connected by a path in the regex language."""
    graph_fa = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))
    regex_fa = AdjacencyMatrixFA(regex_to_dfa(regex))

    intersection = intersect_automata(graph_fa, regex_fa)
    reach = intersection._reachability_matrix()

    n_dfa = regex_fa.states_count

    result = set()
    for start_index in graph_fa.start_states:
        start_vertex = graph_fa.index_to_state[start_index].value
        for final_index in graph_fa.final_states:
            final_vertex = graph_fa.index_to_state[final_index].value
            if any(
                reach[start_index * n_dfa + dfa_start, final_index * n_dfa + dfa_final]
                for dfa_start in regex_fa.start_states
                for dfa_final in regex_fa.final_states
            ):
                result.add((start_vertex, final_vertex))

    return result
