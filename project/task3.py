from pyformlang.finite_automaton import *
from scipy.sparse import *
from networkx import *
from typing import *

from project import regex_to_dfa, graph_to_nfa

from itertools import product


class FiniteAutomaton:
    def __init__(self, nka=None):
        if nka is None:
            return

        map_index_to_state = {s: i for i, s in enumerate(nka.states)}

        self.map_index_to_state = list(nka.states)

        self.start_states = {map_index_to_state[st] for st in nka.start_states}
        self.final_states = {map_index_to_state[fi] for fi in nka.final_states}

        self.func_to_steps = {}

        states = nka.to_dict()
        n = len(nka.states)

        for symbols in nka.symbols:
            self.func_to_steps[symbols] = dok_matrix((n, n), dtype=bool)
            for key, value in states.items():
                if symbols in value:
                    for fi in (
                        value[symbols]
                        if isinstance(value[symbols], set)
                        else {value[symbols]}
                    ):
                        self.func_to_steps[symbols][
                            map_index_to_state[key], map_index_to_state[fi]
                        ] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        nka = NondeterministicFiniteAutomaton()

        for key, value in self.func_to_steps.items():
            nka.add_transitions(
                [
                    (start, key, end)
                    for (start, end) in product(range(value.shape[0]), repeat=2)
                    if self.func_to_steps[key][start, end]
                ]
            )

        for start_state in self.start_states:
            nka.add_start_state(start_state)

        for final_state in self.final_states:
            nka.add_final_state(final_state)

        return nka.accepts(word)

    def is_empty(self) -> bool:
        if len(self.func_to_steps) == 0:
            return True

        dka = sum(self.func_to_steps.values())

        for _ in range(dka.shape[0]):
            dka += dka @ dka

        for st, fi in product(self.start_states, self.final_states):
            if dka[st, fi] != 0:
                return False

        return True


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:

    commaon_keys = automaton1.func_to_steps.keys() & automaton2.func_to_steps.keys()
    finatie_automaton = FiniteAutomaton()
    finatie_automaton.func_to_steps = {}

    for key in commaon_keys:
        finatie_automaton.func_to_steps[key] = kron(
            automaton1.func_to_steps[key], automaton2.func_to_steps[key], "csr"
        )

    finatie_automaton.start_states = set()
    finatie_automaton.final_states = set()

    n_states2 = automaton2.func_to_steps.values().__iter__().__next__().shape[0]

    for m, k in product(automaton1.start_states, automaton2.start_states):
        finatie_automaton.start_states.add(m * (n_states2) + k)

    for m, k in product(automaton1.final_states, automaton2.final_states):
        finatie_automaton.final_states.add(m * (n_states2) + k)

    return finatie_automaton


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list[tuple[int, int]]:
    fa1 = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    fa2 = FiniteAutomaton(regex_to_dfa(regex))

    finite_automaton = intersect_automata(fa1, fa2)

    if len(finite_automaton.func_to_steps) == 0:
        return []

    m = sum(finite_automaton.func_to_steps.values())

    for _ in range(m.shape[0]):
        m += m @ m

    n_states2 = fa2.func_to_steps.values().__iter__().__next__().shape[0]

    def convert_to_node(i):
        return fa1.map_index_to_state[i // n_states2].value

    res = []
    for st, fi in product(finite_automaton.start_states, finite_automaton.final_states):
        if m[st, fi] != 0:
            res.append((convert_to_node(st), convert_to_node(fi)))

    return res
