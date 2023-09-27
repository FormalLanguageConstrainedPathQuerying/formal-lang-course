from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse


class BoolMatrix:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        self.start_states, self.final_states = set(), set()
        self.states, self.matrices = dict(), dict()

        if nfa is None:
            return

        for i, state in enumerate(nfa.states):
            self.states[state] = i
        for state in nfa.start_states:
            self.start_states.add(self.states[state])
        for state in nfa.final_states:
            self.final_states.add(self.states[state])

        num_of_states = len(self.states)

        for start_state, transitions in nfa.to_dict().items():
            for symbol, finish_states in transitions.items():
                if isinstance(finish_states, State):
                    finish_states = {finish_states}

                for finish_state in finish_states:
                    if symbol not in self.matrices:
                        self.matrices[symbol] = sparse.csr_matrix(
                            (num_of_states, num_of_states), dtype=bool
                        )

                    self.matrices[symbol][
                        self.states[start_state], self.states[finish_state]
                    ] = True

    def intersect(self, other: "BoolMatrix"):
        result = BoolMatrix()

        for symbol in self.matrices.keys() & other.matrices.keys():
            result.matrices[symbol] = sparse.kron(
                self.matrices[symbol], other.matrices[symbol], format="csr"
            )

        for _, self_index in self.states.items():
            for _, other_index in other.states.items():
                result_state = self_index * len(other.states) + other_index
                result.states[result_state] = result_state

                if (
                    self_index in self.start_states
                    and other_index in other.start_states
                ):
                    result.start_states.add(result_state)

                if (
                    self_index in self.final_states
                    and other_index in other.final_states
                ):
                    result.final_states.add(result_state)

        return result

    def transitive_closure(self):
        if len(self.matrices) == 0:
            return sparse.csr_matrix((0, 0), dtype=bool)

        result = sum(self.matrices.values())
        prev_nnz = 0
        while result.nnz != prev_nnz:
            prev_nnz = result.nnz
            result += result @ result

        return result

    def to_nfa(self):
        nfa = NondeterministicFiniteAutomaton()
        for symbol, matrix in self.matrices.items():
            for start_state, finish_state in zip(*matrix.nonzero()):
                nfa.add_transition(start_state, symbol, finish_state)

        for state in self.start_states:
            nfa.add_start_state(state)

        for state in self.final_states:
            nfa.add_final_state(state)

        return nfa
