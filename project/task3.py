from symtable import Symbol
from networkx import MultiDiGraph
from pyformlang.finite_automaton import (
    DeterministicFiniteAutomaton,
    NondeterministicFiniteAutomaton,
    State,
)
from scipy.sparse import dok_matrix, kron
from project.task2 import graph_to_nfa, regex_to_dfa
from typing import Dict, Set, Iterable


class FiniteAutomaton:
    transition_function: Dict
    starts_states: Set
    finals_states: Set
    states_to_index: Set
    symbols_to_index: Set
    is_symbols: bool

    def __init__(
        self,
        dka: DeterministicFiniteAutomaton = None,
        nka: NondeterministicFiniteAutomaton = None,
        transition_function_state: Dict = None,
        transition_function_symbols: Dict = None,
        states_to_index: Set = None,
        symbols_to_index: Set = None,
        start_stare: Set = None,
        final_state: Set = None,
    ) -> None:
        if dka or nka:
            ka = dka if dka else nka

            self.starts_states = ka.start_state
            self.finals_states = ka.final_states

            states = ka.to_dict()
            transition_function_state = dict()
            self.is_symbols = False
            self.states_to_index = {v: i for i, v in enumerate(ka.states)}
            self.symbols_to_index = {v: i for i, v in enumerate(ka.symbols)}

            for state, state_index in self.states_to_index.items():
                transition_function_state[state_index] = dok_matrix(
                    (len(ka.symbols), len(ka.states)), dtype=bool
                )

            for u, e in states.items():
                for symbol in ka.symbols:
                    if symbol in e:
                        vs = e[symbol] if isinstance(e[symbol], set) else [e[symbol]]
                        for v in vs:
                            transition_function_state[self.states_to_index[u]][
                                self.symbols_to_index[symbol], self.states_to_index[v]
                            ] = True

            self.transition_function = transition_function_state

            return

        if transition_function_state and start_stare and final_state:
            self.is_symbols = False
            self.starts_states = start_stare
            self.finals_states = final_state
            self.transition_function = transition_function_state
            self.states_to_index = states_to_index
            self.symbols_to_index = symbols_to_index

            return

        if start_stare and final_state:
            self.is_symbols = True
            self.starts_states = start_stare
            self.finals_states = final_state
            self.transition_function = transition_function_symbols
            self.states_to_index = states_to_index
            self.symbols_to_index = symbols_to_index

            return

        raise RuntimeError("Invalid input by class FiniteAutomaton")

    def transition_function_state_to_nka(self) -> NondeterministicFiniteAutomaton:
        nka: NondeterministicFiniteAutomaton = NondeterministicFiniteAutomaton()

        for state, state_index in self.states_to_index.items():
            for symbol, symbol_index in self.symbols_to_index.items():
                for end_index, value in enumerate(
                    self.transition_function[state_index][symbol_index,]
                    .toarray()
                    .flatten()
                ):
                    if value:
                        nka.add_transition(state_index, symbol, end_index)

        for start_state in self.starts_states:
            nka.add_start_state(self.states_to_index[start_state])

        for final_state in self.finals_states:
            nka.add_start_state(self.states_to_index[final_state])

        return nka

    def transition_function_symbols_to_nka(self) -> NondeterministicFiniteAutomaton:
        nka: NondeterministicFiniteAutomaton = NondeterministicFiniteAutomaton()

        for symbol, symbol_index in self.symbols_to_index.items():
            for state, state_index in self.states_to_index.items():
                for end_index, value in enumerate(
                    self.transition_function[symbol][state_index,].toarray().flatten()
                ):
                    if value:
                        nka.add_transition(state_index, symbol, end_index)

        for start_state in self.starts_states:
            nka.add_start_state(self.states_to_index[start_state])

        for final_state in self.finals_states:
            nka.add_start_state(self.states_to_index[final_state])

        return nka

    def accepts(self, word: Iterable[Symbol]) -> bool:
        if self.is_empty():
            return True

        nka: NondeterministicFiniteAutomaton = None

        if self.is_symbols:
            nka = self.transition_function_symbols_to_nka()
        else:
            nka = self.transition_function_state_to_nka()

        return not nka.accepts(word)

    def is_empty(self) -> bool:
        return len(self.transition_function) == 0


def transition_function_statate_to_sym_convert(automaton1: FiniteAutomaton):
    automaton1_transition_function: Dict = dict()

    for symbol, symbol_index in automaton1.symbols_to_index.items():
        automaton1_transition_function[symbol] = dok_matrix(
            (
                len(automaton1.states_to_index.keys()),
                len(automaton1.states_to_index.keys()),
            ),
            dtype=bool,
        )

    for state, state_index in automaton1.states_to_index.items():
        for symbol, symbol_index in automaton1.symbols_to_index.items():
            for end_index, value in enumerate(
                automaton1.transition_function[state_index][symbol_index,]
                .toarray()
                .flatten()
            ):
                if value:
                    automaton1_transition_function[symbol][
                        state_index, end_index
                    ] = True

    return automaton1_transition_function


def intersect_automata(
    automaton1: FiniteAutomaton, automaton2: FiniteAutomaton
) -> FiniteAutomaton:
    automaton1_transition_function: Dict = (
        transition_function_statate_to_sym_convert(automaton1)
        if not automaton1.is_symbols
        else automaton1.transition_function
    )
    automaton2_transition_function: Dict = (
        transition_function_statate_to_sym_convert(automaton2)
        if not automaton2.is_symbols
        else automaton2.transition_function
    )

    symbols = (
        automaton1_transition_function.keys() & automaton2_transition_function.keys()
    )
    symbols_to_index = {v: i for i, v in enumerate(symbols)}

    transition_function = dict()
    starts_states = set()
    finals_states = set()
    state_to_index = dict()

    s1 = (
        automaton1.starts_states
        if isinstance(automaton1.starts_states, set)
        else [automaton1.starts_states]
    )
    s2 = (
        automaton2.starts_states
        if isinstance(automaton2.starts_states, set)
        else [automaton2.starts_states]
    )

    f1 = (
        automaton1.finals_states
        if isinstance(automaton1.finals_states, set)
        else [automaton1.finals_states]
    )
    f2 = (
        automaton2.finals_states
        if isinstance(automaton2.finals_states, set)
        else [automaton2.finals_states]
    )

    for symbol in symbols:
        transition_function[symbol] = kron(
            automaton1_transition_function[symbol],
            automaton2_transition_function[symbol],
            "csr",
        )

    for u, i in automaton1.states_to_index.items():
        for v, j in automaton2.states_to_index.items():

            k = len(automaton2.states_to_index) * i + j
            state_to_index[k] = k

            assert isinstance(u, State)
            if u in s1 and v in s2:
                starts_states.add(State(k))

            if u in f1 and v in f2:
                finals_states.add(State(k))

    return FiniteAutomaton(
        transition_function_symbols=transition_function,
        start_stare=starts_states,
        final_state=finals_states,
        states_to_index=state_to_index,
        symbols_to_index=symbols_to_index,
    )


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
) -> list:
    automaton1 = FiniteAutomaton(nka=graph_to_nfa(graph=graph))
    automaton2 = FiniteAutomaton(dka=regex_to_dfa(regex=regex))

    final_automete: FiniteAutomaton = intersect_automata(
        automaton1=automaton1, automaton2=automaton2
    )

    return zip(final_automete.starts_states, final_automete.finals_states)
