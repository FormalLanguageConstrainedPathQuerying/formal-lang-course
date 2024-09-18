from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
)
import numpy as np
from scipy.sparse import csr_array


class AdjacencyMatrixFA:
    def __init__(self, dfa: NondeterministicFiniteAutomaton):
        # get FA transitions
        transitions_dict = dfa.to_dict()
        transitions: list[tuple] = list(transitions_dict.items())

        matrix_length = len(transitions)

        row: list[int] = []
        col: list[int] = []
        data: list[int] = []

        self.start_nodes: set[int] = set(int(x) for x in dfa.start_states)
        self.final_nodes: set[int] = set(int(x) for x in dfa.final_states)

        for trans in transitions:
            source_node: int = trans[0]._value
            ways = trans[1].items()

            for way in ways:
                sym: int = int(way[0]._value)
                dest_node: int = way[1]._value

                row.append(source_node)
                col.append(dest_node)
                data.append(sym)

        # convert it to matrix
        np_row = np.array(row)
        np_col = np.array(col)
        np_data = np.array(data)

        self.sparse_matrix = csr_array(
            (np_data, (np_row, np_col)), shape=(max(row) + 1, max(col) + 1)
        )


fa = DeterministicFiniteAutomaton()
fa.add_transitions([(0, 1, 4), (0, 2, 3), (1, 3, 5)])

amf = AdjacencyMatrixFA(fa)
print(amf.sparse_matrix)
