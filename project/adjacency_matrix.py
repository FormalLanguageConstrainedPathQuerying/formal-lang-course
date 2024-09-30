import itertools
from collections import defaultdict
from functools import reduce
from typing import Any, Iterable, Optional, cast

from networkx import MultiDiGraph
import numpy as np
from numpy.typing import NDArray
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    Symbol,
    FiniteAutomaton,
)
from scipy.sparse import csr_array, csr_matrix, kron

from project.finite_automaton import graph_to_nfa, regex_to_dfa


class AdjacencyMatrixFA:
    def __init__(self, fa: FiniteAutomaton):
        graph = fa.to_networkx()
        self.states_count = graph.number_of_nodes()
        self.states = {state: i for i, state in enumerate(fa.states)}
        self.final_states = {self.states[state] for state in fa.final_states}
        self.start_states = {self.states[state] for state in fa.start_states}

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

    new_amf = AdjacencyMatrixFA(DeterministicFiniteAutomaton())
    new_amf.states_count = amf1.states_count * amf2.states_count

    for state1, state2 in itertools.product(amf1.states.keys(), amf2.states.keys()):
        i1, i2 = amf1.states[state1], amf2.states[state2]
        new_i = amf2.states_count * i1 + i2
        new_amf.states[(state1, state2)] = new_i

        if i1 in amf1.start_states and i2 in amf2.start_states:
            new_amf.start_states.add(new_i)
        if i1 in amf1.final_states and i2 in amf2.final_states:
            new_amf.final_states.add(new_i)

    for sym, am1 in amf1.matrices.items():
        if (am2 := amf2.matrices.get(sym)) is None:
            continue
        new_amf.matrices[sym] = cast(csr_array, kron(am1, am2, format="csr"))

    return new_amf


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    regex_amf = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_amf = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))
    inter = intersect_automata(regex_amf, graph_amf)
    closure = inter.transitive_closure()
    regex_start_states = [
        key
        for key in regex_amf.states
        if regex_amf.states[key] in regex_amf.start_states
    ]
    regex_final_states = [
        key
        for key in regex_amf.states
        if regex_amf.states[key] in regex_amf.final_states
    ]
    graph_start_states = [
        key
        for key in graph_amf.states
        if graph_amf.states[key] in graph_amf.start_states
    ]
    graph_final_states = [
        key
        for key in graph_amf.states
        if graph_amf.states[key] in graph_amf.final_states
    ]
    all_states = itertools.product(
        graph_start_states,
        graph_final_states,
        regex_start_states,
        regex_final_states,
    )
    res = set(
        (start, final)
        for start, final, regex_start, regex_final in all_states
        if closure[
            inter.states[(regex_start, start)],
            inter.states[(regex_final, final)],
        ]
    )
    return res
