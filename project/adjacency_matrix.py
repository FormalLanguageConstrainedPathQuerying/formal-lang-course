from collections import defaultdict
import itertools
from typing import Any, Iterable, Optional
from networkx.classes.reportviews import NodeView
from numpy.typing import NDArray
import numpy as np
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    DeterministicFiniteAutomaton,
    Symbol,
)
from scipy.sparse import csr_array, kron, csr_matrix
from functools import reduce


class AdjacencyMatrixFA:
    def __init__(self, nfa: NondeterministicFiniteAutomaton):
        graph = nfa.to_networkx()
        self.states_count = graph.number_of_nodes()
        self.states = {state: i for i, state in enumerate(nfa.states)}
        self.final_states = {self.states[state] for state in nfa.final_states}
        self.start_states = {self.states[state] for state in nfa.start_states}

        transitions: dict[Symbol, NDArray] = defaultdict(
            lambda: np.zeros((self.states_count, self.states_count), dtype=np.bool_)
        )

        edges: Iterable[tuple[Any, Any, Any]] = graph.edges(data="label")
        transit = (
            (self.states[st1], self.states[st2], Symbol(lable))
            for st1, st2, lable in edges
        )
        for idx1, idx2, symbol in transit:
            transitions[symbol][idx1, idx2] = True

        self.matrices: dict[Symbol, csr_array] = {
            sym: csr_array(matrix) for (sym, matrix) in transitions.items()
        }

    def accepts(self, word: Iterable[Symbol]) -> bool:
        chars = list(word)
        inits = [(state, chars) for state in self.start_states]

        while len(inits) > 0:
            state, tail = inits.pop()

            if not tail and state in self.final_states:
                return True

            first_ch, *rem = tail
            for follow in self.states.values():
                if self.matrices[first_ch][state, follow]:
                    inits.append((state, rem))

        return False

    def transitive_closure(self) -> csr_matrix:
        base = csr_matrix((self.states_count, self.states_count), dtype=bool)
        base.setdiag(True)

        if not self.matrices:
            return base

        reach: csr_matrix = base + reduce(lambda x, y: x + y, self.matrices.values())

        for i, j, k in itertools.product(range(self.states_count), repeat=3):
            reach[j, k] = reach[j, k] or (reach[j, i] and reach[i, k])

        return reach

    def is_empty(self) -> bool:
        closure = self.transitive_closure()

        for start_state, final_state in itertools.product(
            self.start_states, self.final_states
        ):
            if closure[start_state, final_state]:
                return False
        return True
