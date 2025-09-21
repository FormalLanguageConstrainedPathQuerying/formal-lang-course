from typing import Iterable
from networkx import MultiDiGraph
from pyformlang.finite_automaton import State, Symbol, NondeterministicFiniteAutomaton
from scipy.sparse import identity, kron, csr_matrix, lil_matrix

from project.build_graph import regex_to_dfa, graph_to_nfa


class AdjacencyMatrixFA:
    def __init__(self, finite_automaton: NondeterministicFiniteAutomaton):
        self.states = finite_automaton.states
        self.labels = finite_automaton.symbols
        self.start_states = (
            finite_automaton.start_states
            if isinstance(finite_automaton.start_states, set)
            else {finite_automaton.start_states}
        )
        self.final_states = (
            finite_automaton.final_states
            if isinstance(finite_automaton.final_states, set)
            else {finite_automaton.final_states}
        )

        state_list = list(self.states)
        self.state_to_index = {state: idx for idx, state in enumerate(state_list)}
        self.index_to_state = {idx: state for idx, state in enumerate(state_list)}
        self.transition_matrices = self._build_transition_matrices(finite_automaton)

    def _build_transition_matrices(
        self, finite_automaton: NondeterministicFiniteAutomaton
    ) -> dict[Symbol, csr_matrix]:
        transition_matrices = {}
        automaton_transitions = finite_automaton.to_dict()
        size = len(self.states)

        for symbol in self.labels:
            matrix = lil_matrix((size, size), dtype=bool)
            for source_state in self.states:
                if source_state not in automaton_transitions:
                    continue
                state_transitions = automaton_transitions[source_state]
                if symbol not in state_transitions:
                    continue
                destination_states = state_transitions[symbol]
                if not isinstance(destination_states, set):
                    destination_states = {destination_states}
                source_idx = self.state_to_index[source_state]
                for destination_state in destination_states:
                    matrix[source_idx, self.state_to_index[destination_state]] = True
            transition_matrices[symbol] = matrix.tocsr()
        return transition_matrices

    def get_trans_closure(self) -> csr_matrix:
        if not self.transition_matrices:
            return identity(len(self.states), format="csr", dtype=bool)
        combined = identity(len(self.states), format="csr", dtype=bool)
        for matrix in self.transition_matrices.values():
            combined += matrix
        closure = combined.copy()
        prev_nnz = closure.nnz
        for _ in range(len(self.states)):
            closure = closure @ combined
            if closure.nnz == prev_nnz:
                break
            prev_nnz = closure.nnz
        return closure

    def is_empty(self) -> bool:
        if not self.start_states or not self.final_states:
            return True
        closure = self.get_trans_closure()
        return not any(
            closure[self.state_to_index[start_state], self.state_to_index[final_state]]
            for start_state in self.start_states
            for final_state in self.final_states
        )

    def accepts(self, word: Iterable[Symbol]) -> bool:
        current_states = self.start_states.copy()
        for symbol in word:
            if symbol not in self.transition_matrices:
                return False
            next_states = {
                self.index_to_state[dest_idx]
                for source_state in current_states
                for dest_idx in self.transition_matrices[symbol][
                    self.state_to_index[source_state]
                ].indices
            }
            current_states = next_states
            if not current_states:
                return False
        return bool(current_states & self.final_states)

    @classmethod
    def _with_index_mapping(
        cls,
        finite_automaton: NondeterministicFiniteAutomaton,
        state_to_index: dict[State, int],
        index_to_state: dict[int, State],
    ) -> "AdjacencyMatrixFA":
        instance = cls.__new__(cls)
        instance.states = finite_automaton.states
        instance.labels = finite_automaton.symbols
        instance.start_states = (
            finite_automaton.start_states
            if isinstance(finite_automaton.start_states, set)
            else {finite_automaton.start_states}
        )
        instance.final_states = (
            finite_automaton.final_states
            if isinstance(finite_automaton.final_states, set)
            else {finite_automaton.final_states}
        )
        instance.state_to_index = state_to_index
        instance.index_to_state = index_to_state
        instance.transition_matrices = instance._build_transition_matrices(
            finite_automaton
        )
        return instance

    @staticmethod
    def from_matrices(
        states: set[State],
        start_states: set[State],
        final_states: set[State],
        state_to_index: dict[State, int],
        index_to_state: dict[int, State],
        transition_matrices: dict[Symbol, csr_matrix],
    ) -> "AdjacencyMatrixFA":
        nfa = NondeterministicFiniteAutomaton(
            states=states, start_state=start_states, final_states=final_states
        )
        for symbol, matrix in transition_matrices.items():
            for source_idx, dest_idx in zip(*matrix.nonzero()):
                nfa.add_transition(
                    index_to_state[source_idx], symbol, index_to_state[dest_idx]
                )
        return AdjacencyMatrixFA._with_index_mapping(
            nfa, state_to_index, index_to_state
        )


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    states1, states2 = list(automaton1.states), list(automaton2.states)
    size2 = len(states2)

    intersection_states = set()
    state_to_index = {}
    index_to_state = {}

    for i, state1 in enumerate(states1):
        for j, state2 in enumerate(states2):
            intersection_state = State((state1, state2))
            intersection_states.add(intersection_state)
            intersection_idx = i * size2 + j
            state_to_index[intersection_state] = intersection_idx
            index_to_state[intersection_idx] = intersection_state

    start_states = {
        State((s1, s2))
        for s1 in automaton1.start_states
        for s2 in automaton2.start_states
    }
    final_states = {
        State((s1, s2))
        for s1 in automaton1.final_states
        for s2 in automaton2.final_states
    }
    shared_symbols = automaton1.labels & automaton2.labels
    transition_matrices = {
        symbol: kron(
            automaton1.transition_matrices[symbol],
            automaton2.transition_matrices[symbol],
            format="csr",
        )
        for symbol in shared_symbols
    }

    return AdjacencyMatrixFA.from_matrices(
        intersection_states,
        start_states,
        final_states,
        state_to_index,
        index_to_state,
        transition_matrices,
    )


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    intersection = intersect_automata(
        AdjacencyMatrixFA(regex_to_dfa(regex)),
        AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes)),
    )
    closure = intersection.get_trans_closure()
    return {
        (start_state.value[1], final_state.value[1])
        for start_state in intersection.start_states
        for final_state in intersection.final_states
        if closure[
            intersection.state_to_index[start_state],
            intersection.state_to_index[final_state],
        ]
    }
