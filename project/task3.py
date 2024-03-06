from symtable import Symbol
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
import numpy as np
from scipy.sparse import dok_matrix, kron

from typing import Dict, Set, Iterable, Any

from project.task2 import graph_to_nfa, regex_to_dfa


class FiniteAutomaton:
    transition_function: Dict
    starts_states: Set
    finals_states: Set
    states_to_index: Set
    symbols_to_index: Set

    def __init__(
        self,
        dka: DeterministicFiniteAutomaton = None,
        nka: NondeterministicFiniteAutomaton = None,
        sparce_row: dok_matrix = None,
        start_stare: Set = None,
        final_state: Set = None,
    ) -> None:
        if dka or nka:
            ka = dka if dka else nka

            self.starts_states = ka.start_state
            self.finals_states = ka.final_states

            states = ka.to_dict()
            transition_function = dict()
            self.states_to_index = {v: i for i, v in enumerate(ka.states)}
            self.symbols_to_index = {v: i for i, v in enumerate(ka.symbols)}

            for u, e in states.items():
                transition_function[self.states_to_index[u]] = dok_matrix((len(ka.symbols), len(ka.states)), dtype=bool)
                for symbol in ka.symbols:
                    if symbol in e:
                        vs = e[symbol] if isinstance(e[symbol], set) else [e[symbol]]
                        for v in vs:
                            transition_function[self.states_to_index[u]][self.symbols_to_index[symbol], self.states_to_index[v]] = True

            self.transition_function = transition_function

            return

        if sparce_row and start_stare and final_state:
            self.starts_states = start_stare
            self.finals_states = final_state
            self.transition_function = sparce_row

            return

        raise RuntimeError("Invalid input by class FiniteAutomaton")

    def accepts(self, word: Iterable[Symbol]) -> bool:
        nka: NondeterministicFiniteAutomaton = NondeterministicFiniteAutomaton()

        for state, state_index in self.states_to_index.items():
            for symbol, symbol_index in self.symbols_to_index.items():
                for end_index in self.transition_function[state_index][state_index,]:
                    if end_index:
                        nka.add_transition(state_index, symbol, end_index)

        for start_state in self.starts_states:
            nka.add_start_state(self.states_to_index[start_state])

        for final_state in self.finals_states:
            nka.add_start_state(self.states_to_index[final_state])

        return nka.accepts("".join(list(word)))

    def is_empty(self) -> bool:
        return len(self.transition_function) == 0


def intersect_automata(automaton1: FiniteAutomaton, automaton2: FiniteAutomaton) -> FiniteAutomaton:
    intersect_transition_function = {}

    for state1 in automaton1.transition_function.keys():
        for state2 in automaton2.transition_function.keys():
            matrix1 = automaton1.transition_function[state1]
            matrix2 = automaton2.transition_function[state2]

            intersect_matrix = matrix1.dot(matrix2)

            intersect_transition_function[state1] = intersect_matrix

    intersect_automaton = FiniteAutomaton(sparce_row=intersect_transition_function,
                                          start_stare=automaton1.starts_states,
                                          final_state=automaton1.finals_states)

    return intersect_automaton