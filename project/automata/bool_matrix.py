from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State
from scipy import sparse


class BoolMatrix:
    def __init__(self, nfa: NondeterministicFiniteAutomaton = None):
        if nfa is None:
            self.start_states, self.final_states = set(), set()
            self.num_of_states = 0
            self.states, self.matrices = dict(), dict()
            return

        self.num_of_states = len(nfa.states)
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
