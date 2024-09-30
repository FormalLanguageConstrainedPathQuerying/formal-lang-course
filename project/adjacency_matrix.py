import itertools
from collections import defaultdict
from functools import reduce
from typing import Any, Iterable, Optional, cast

import numpy as np
from numpy.typing import NDArray
from pyformlang.finite_automaton import (
    NondeterministicFiniteAutomaton,
    Symbol,
    FiniteAutomaton,
)
from scipy.sparse import csr_array, csr_matrix, kron


class AdjacencyMatrixFA:
    def __init__(self, nfa: FiniteAutomaton):
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
            if lable
        )
        for idx1, idx2, symbol in transit:
            transitions[symbol][idx1, idx2] = True

        self.matrices: dict[Symbol, csr_array] = {
            sym: csr_array(matrix) for (sym, matrix) in transitions.items()
        }

    def accepts(self, word: Iterable[Symbol]) -> bool:
        chars = list(word)
        inits = [(state, chars) for state in self.start_states]

        while inits:
            state, tail = inits.pop()

            if not tail:
                if state in self.final_states:
                    return True
                continue

            first_ch, *rem = tail

            for follow in self.states.values():
                if self.matrices[first_ch][state, follow]:
                    inits.append((follow, rem))

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


def intersect_automata(
    amf1: AdjacencyMatrixFA, amf2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:

    new_amf = AdjacencyMatrixFA(FiniteAutomaton())
    new_amf.states_count = amf1.states_count * amf2.states_count

    for sym, adj1 in amf1.matrices.items():
        if (adj2 := amf2.matrices.get(sym)) is None:
            continue
        new_amf.matrices[sym] = cast(csr_array, kron(adj1, adj2, format="csr"))

    for state1, state2 in itertools.product(amf1.states.keys(), amf2.states.keys()):
        i1, i2 = amf1.states[state1], amf2.states[state2]
        new_i = amf2.states_count * i1 + i2
        new_amf.states[(state1, state2)] = new_i

        if i1 in amf1.start_states and i2 in amf2.start_states:
            new_amf.start_states.add(new_i)
        if i1 in amf1.final_states and i2 in amf2.final_states:
            new_amf.final_states.add(new_i)

    return new_amf
