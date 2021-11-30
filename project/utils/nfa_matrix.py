from scipy.sparse import kron
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State

from project.utils.boolean_matrix import BooleanMatrix


class NFAMatrix(BooleanMatrix):
    """
    Representation of NFA as a Boolean Matrix
    """

    def __init__(self):
        super().__init__()

    def to_nfa(self):
        """
        Transforms BooleanMatrix into NFA

        Returns
        -------
        nfa: NondeterministicFiniteAutomaton
            Representation of BooleanMatrix as NFA
        """
        nfa = NondeterministicFiniteAutomaton()
        for label in self.bmatrix.keys():
            arr = self.bmatrix[label].toarray()
            for i in range(len(arr)):
                for j in range(len(arr)):
                    if arr[i][j]:
                        from_state = (
                            State((i // self.block_size, i % self.block_size))
                            if self.block_size > 1
                            else State(i)
                        )
                        to_state = (
                            State((j // self.block_size, j % self.block_size))
                            if self.block_size > 1
                            else State(j)
                        )
                        nfa.add_transition(
                            self.indexed_states[from_state],
                            label,
                            self.indexed_states[to_state],
                        )

        for start_state in self.start_states:
            nfa.add_start_state(self.indexed_states[State(start_state)])
        for final_state in self.final_states:
            nfa.add_final_state(self.indexed_states[State(final_state)])

        return nfa
