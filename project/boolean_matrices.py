from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    State,
    EpsilonNFA,
)
from scipy import sparse
from scipy.sparse import dok_matrix

from project.rsm import RSM


class BooleanMatrices:
    def __init__(
        self,
        state_to_index: dict,
        start_states: set,
        final_states: set,
        bool_matrices: dict,
    ):
        self.state_to_index = state_to_index
        self.start_states = start_states
        self.final_states = final_states
        self.bool_matrices = bool_matrices
        self.num_states = len(self.state_to_index.keys())

    @staticmethod
    def _create_boolean_matrices(nfa: EpsilonNFA, state_to_index: dict[State, int]):
        b_matrices = {}
        for state_from, transition in nfa.to_dict().items():
            for label, states_to in transition.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = state_to_index[state_from]
                    index_to = state_to_index[state_to]

                    if label not in b_matrices:
                        b_matrices[label] = sparse.dok_matrix(
                            (len(nfa.states), len(nfa.states)), dtype=bool
                        )

                    b_matrices[label][index_from, index_to] = True

        return b_matrices

    @classmethod
    def from_automaton(cls, nfa: EpsilonNFA) -> "BooleanMatrices":
        state_to_index = {state: index for index, state in enumerate(nfa.states)}
        return cls(
            state_to_index,
            nfa.start_states.copy(),
            nfa.final_states.copy(),
            cls._create_boolean_matrices(nfa, state_to_index),
        )

    @classmethod
    def from_rsm(cls, rsm: RSM) -> "BooleanMatrices":
        states, start_states, final_states = set(), set(), set()
        for v, dfa in rsm.boxes.items():
            for s in dfa.states:
                state = State((v, s.value))
                states.add(state)
                if s in dfa.start_states:
                    start_states.add(state)
                if s in dfa.final_states:
                    final_states.add(state)

        states = sorted(states, key=lambda s: s.value)
        state_to_index = {s: i for i, s in enumerate(states)}
        bool_matrices = dict()

        for v, dfa in rsm.boxes.items():
            for state_from, transitions in dfa.to_dict().items():
                for label, states_to in transitions.items():
                    states_to = states_to if isinstance(states_to, set) else {states_to}
                    for state_to in states_to:
                        if label not in bool_matrices:
                            bool_matrices[label] = dok_matrix(
                                (len(states), len(states)), dtype=bool
                            )

                        i = state_to_index[State((v, state_from.value))]
                        j = state_to_index[State((v, state_to.value))]
                        bool_matrices[label][i, j] = True
        return cls(
            state_to_index,
            start_states,
            final_states,
            bool_matrices,
        )

    def to_automaton(self):
        nfa = NondeterministicFiniteAutomaton()

        for symbol, matrix in self.bool_matrices.items():
            rows, columns = matrix.nonzero()
            for row, column in zip(rows, columns):
                nfa.add_transition(row, symbol, column)

        for state in self.start_states:
            nfa.add_start_state(state)

        for state in self.final_states:
            nfa.add_final_state(state)

        return nfa

    def transitive_closure(self: "BooleanMatrices") -> dok_matrix:
        if not self.bool_matrices.values():
            return dok_matrix((1, 1))
        transitive_closure = sum(self.bool_matrices.values())
        prev_nnz = transitive_closure.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, new_nnz = new_nnz, transitive_closure.nnz

        return transitive_closure

    def intersect(
        self: "BooleanMatrices", another: "BooleanMatrices"
    ) -> "BooleanMatrices":
        bool_matrices = dict()
        for label in self.bool_matrices.keys() & another.bool_matrices.keys():
            bool_matrices[label] = sparse.kron(
                self.bool_matrices[label], another.bool_matrices[label], format="dok"
            )

        state_to_index = dict()
        start_states, final_states = set(), set()
        for s1, s1_index in self.state_to_index.items():
            for s2, s2_index in another.state_to_index.items():
                index = s1_index * another.num_states + s2_index
                state = index
                state_to_index[state] = index

                if s1 in self.start_states and s2 in another.start_states:
                    start_states.add(state)

                if s1 in self.final_states and s2 in another.final_states:
                    final_states.add(state)

        return BooleanMatrices(
            state_to_index, start_states, final_states, bool_matrices
        )

    def get_start_states(self):
        return self.start_states.copy()

    def get_final_states(self):
        return self.final_states.copy()

    def get_state_by_index(self, index):
        for state, idx in self.state_to_index.items():
            if idx == index:
                return state

    def direct_sum(self, other: "BooleanMatrices"):
        common_symbols = self.bool_matrices.keys() & other.bool_matrices.keys()
        bool_matrices = dict()
        for symbol in common_symbols:
            bool_matrices[symbol] = sparse.bmat(
                [
                    [self.bool_matrices[symbol], None],
                    [None, other.bool_matrices[symbol]],
                ]
            )

        state_to_index = dict()
        start_states, final_states = set(), set()
        for state, index in self.state_to_index.items():
            state_to_index[state] = index

            # если состояние является стартовым у одной из матриц, то и у матрицы прямой суммы оно тоже будет стартовым
            if state in self.start_states:
                start_states.add(state)

            if state in self.final_states:
                final_states.add(state)

        for state, index in other.state_to_index.items():
            new_state = State(state.value + self.num_states)
            state_to_index[new_state] = index + self.num_states

            if state in other.start_states:
                start_states.add(new_state)

            if state in other.final_states:
                final_states.add(new_state)

        return BooleanMatrices(
            state_to_index, start_states, final_states, bool_matrices
        )
