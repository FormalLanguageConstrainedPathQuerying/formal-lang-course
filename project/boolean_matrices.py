from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from scipy import sparse
from scipy.sparse import dok_matrix


class BooleanMatrices:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.num_states = 0
            self.start_states = set()
            self.final_states = set()
            self.bool_matrices = dict()
            self.state_indexes = dict()
        else:
            self.num_states = len(nfa.states)
            self.start_states = nfa.start_states
            self.final_states = nfa.final_states
            self.state_indexes = {
                state: index for index, state in enumerate(nfa.states)
            }
            self.bool_matrices = self._create_boolean_matrices(nfa)

    def _create_boolean_matrices(self, nfa: NondeterministicFiniteAutomaton):
        b_matrices = {}
        for state_from, transition in nfa.to_dict().items():
            for label, states_to in transition.items():
                if not isinstance(states_to, set):
                    states_to = {states_to}
                for state_to in states_to:
                    index_from = self.state_indexes[state_from]
                    index_to = self.state_indexes[state_to]

                    if label not in b_matrices:
                        b_matrices[label] = sparse.dok_matrix(
                            (self.num_states, self.num_states), dtype=bool
                        )

                    b_matrices[label][index_from, index_to] = True

        return b_matrices

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

    def transitive_closure(self):
        if not self.bool_matrices.values():
            return dok_matrix((1, 1))
        transitive_closure = sum(self.bool_matrices.values())
        prev_nnz = transitive_closure.nnz
        new_nnz = 0

        while prev_nnz != new_nnz:
            transitive_closure += transitive_closure @ transitive_closure
            prev_nnz, new_nnz = new_nnz, transitive_closure.nnz

        return transitive_closure

    def intersect(self, another):
        bm = BooleanMatrices()
        bm.num_states = self.num_states * another.num_states

        for label in self.bool_matrices.keys() & another.bool_matrices.keys():
            bm.bool_matrices[label] = sparse.kron(
                self.bool_matrices[label], another.bool_matrices[label], format="dok"
            )

        for s1, s1_index in self.state_indexes.items():
            for s2, s2_index in another.state_indexes.items():
                s_index = s1_index * another.num_states + s2_index
                s = s_index
                bm.state_indexes[s] = s_index

                if s1 in self.start_states and s2 in another.start_states:
                    bm.start_states.add(s)

                if s1 in self.final_states and s2 in another.final_states:
                    bm.final_states.add(s)

        return bm

    def get_start_states(self):
        return self.start_states.copy()

    def get_final_states(self):
        return self.final_states.copy()
