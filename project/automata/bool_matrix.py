from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse


class BoolMatrix:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.start_states, self.final_states = set(), set()
            self.num_of_states = 0
            self.states, self.matrices = dict(), dict()
            return

        self.start_states = nfa.start_states
        self.final_states = nfa.final_states
        self.states = {state: i for i, state in enumerate(nfa.states)}
        self.matrices = dict()
        for start_state, transitions in nfa.to_dict().items():
            for symbol, finish_states in transitions.items():
                if isinstance(finish_states, State):
                    finish_states = {finish_states}

                for finish_state in finish_states:
                    if symbol not in self.matrices:
                        self.matrices[symbol] = sparse.csr_matrix(
                            (self.num_of_states, self.num_of_states), dtype=bool
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

        for self_state, self_index in self.states.items():
            for other_state, other_index in other.states.items():
                result_state = self_state * len(other.states) + other_index
                result.states[result_state] = result_state

                if (
                    self_state in self.start_states
                    and other_state in other.start_states
                ):
                    result.start_states.add(result_state)

                if (
                    self_state in self.final_states
                    and other_state in other.final_states
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
