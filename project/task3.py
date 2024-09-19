from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    State,
    Symbol,
)
import numpy as np
from numpy.typing import NDArray
from scipy.sparse import csr_array
from typing import Iterable


class AdjacencyMatrixFA:
    def __init__(self, fa: NondeterministicFiniteAutomaton):
        # get FA transitions
        transitions_dict = fa.to_dict()
        transitions: list[tuple] = list(transitions_dict.items())

        # set start / final nodes
        self.start_nodes: set[int] = set(int(x) for x in fa.start_states)
        self.final_nodes: set[int] = set(int(x) for x in fa.final_states)

        # dictionary for bool decomposition
        matrices_dict: dict[Symbol, NDArray[np.bool_]] = {}

        self.states_count = len(fa.states)
        matrix_shape = (self.states_count, self.states_count)
        # ^ there may be an error, since there may be states that are not in order

        for trans in transitions:
            # trans = (source_node, {sym: dest_node , ...})
            source_node: int = int(trans[0]._value)
            dests = trans[1].items()

            for dest in dests:
                # DFA: dest = (sym, dest_node)
                # NFA: dest = (sym, {dest_node})
                sym: Symbol = dest[0]._value

                if matrices_dict.get(sym) is None:
                    matrices_dict[sym] = np.zeros(shape=matrix_shape, dtype=np.bool_)

                if isinstance(fa, DeterministicFiniteAutomaton):
                    dest_node: int = dest[1]._value

                    matrices_dict[sym][source_node, dest_node] = True

                elif isinstance(fa, NondeterministicFiniteAutomaton):
                    dest_nodes: dict[int] = dest[1]

                    for dest_node in dest_nodes:
                        dest_node = dest_node._value
                        matrices_dict[sym][source_node, dest_node] = True

        # transform to sparse matrices
        self.sparse_matrices: dict[Symbol, csr_array] = {}

        for key in list(matrices_dict.keys()):
            self.sparse_matrices[key] = csr_array(matrices_dict[key], dtype=np.bool_)


fa = NondeterministicFiniteAutomaton()
fa.add_transitions([(0, "a", 1), (0, "b", 2), (1, "c", 2), (1, "a", 0)])

amf = AdjacencyMatrixFA(fa)
