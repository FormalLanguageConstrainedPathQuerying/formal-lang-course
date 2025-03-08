from scipy.sparse import csr_matrix, kron
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, State, Symbol
from typing import Iterable
from networkx import MultiDiGraph
from project.task2 import regex_to_dfa, graph_to_nfa
import numpy as np


class AdjacencyMatrixFA:
    def __init__(self, automaton: NondeterministicFiniteAutomaton = None):
        if automaton is None:
            self.state_to_index = {}
            self.index_to_state = {}
            self.number_of_states = 0
            self.start_states = set()
            self.final_states = set()
            self.bool_decomposition = {}
            return
        self.state_to_index = {}
        self.index_to_state = {}
        for i, s in enumerate(automaton.states):
            self.state_to_index.update({s: i})
            self.index_to_state.update({i: s})
        self.number_of_states = len(automaton.states)
        self.start_states = set(self.state_to_index[i] for i in automaton.start_states)
        self.final_states = set(self.state_to_index[i] for i in automaton.final_states)

        bool_decomposition = {}
        for first_state, symbols_snd_states in automaton.to_dict().items():
            for symbol, second_states in symbols_snd_states.items():
                if type(second_states) is State:
                    second_states = {second_states}
                for second_state in second_states:
                    if symbol not in bool_decomposition:
                        bool_decomposition[symbol] = csr_matrix(
                            (self.number_of_states, self.number_of_states), dtype=bool)
                    bool_decomposition[symbol][self.state_to_index[first_state], self.state_to_index[second_state]] = True
        self.bool_decomposition = bool_decomposition

    def accepts(self, word: Iterable[Symbol]) -> bool:
        current_states = self.start_states
        for symbol in word:
            next_states = set()
            if symbol in self.bool_decomposition:
                transition_matrix = self.bool_decomposition[symbol]

                for current_state in current_states:
                    for next_state in range(self.number_of_states):
                        if transition_matrix[current_state, next_state]:
                            next_states.add(next_state)
            current_states = next_states
        for state in current_states:
            if state in self.final_states:
                return True
            else:
                return False

    def get_transitive_closure(self) -> csr_matrix:
        closure = csr_matrix((self.number_of_states, self.number_of_states), dtype=bool)
        closure.setdiag(True)

        if not self.bool_decomposition:
            return closure

        closure = sum(self.bool_decomposition.values())
        closure.setdiag(True)

        closure = closure.toarray()

        previous_closure = None
        while not np.array_equal(previous_closure, closure):
            previous_closure = closure
            closure = np.dot(closure, closure)
        return closure

    def is_empty(self) -> bool:
        transitive_closure = self.get_transitive_closure()
        for start in self.start_states:
            for final in self.final_states:
                if transitive_closure[start, final]:
                    return False
        return True


def intersect_automata(
        automaton1: AdjacencyMatrixFA,
        automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    new_states = [State((s1, s2)) for s1, i1 in automaton1.state_to_index.items() for s2, i2 in automaton2.state_to_index.items()]
    new_state_to_index = {}
    new_index_to_state = {}
    for idx, st in enumerate(new_states):
        new_state_to_index.update({st: idx})
        new_index_to_state.update({idx: st})
    new_number_of_states = len(new_states)
    new_start_states = set()
    for i1 in automaton1.start_states:
        for i2 in automaton2.start_states:
            new_state = State((automaton1.index_to_state[i1], automaton2.index_to_state[i2]))
            new_start_states.add(new_state_to_index[new_state])
    new_final_states = set()
    for i1 in automaton1.final_states:
        for i2 in automaton2.final_states:
            new_state = State((automaton1.index_to_state[i1], automaton2.index_to_state[i2]))
            new_final_states.add(new_state_to_index[new_state])

    common_symbols = set(automaton1.bool_decomposition.keys()) & set(automaton2.bool_decomposition.keys())

    new_bool_decomposition = {}
    for symbol in common_symbols:
        m1 = automaton1.bool_decomposition[symbol]
        m2 = automaton2.bool_decomposition[symbol]
        new_matrix = kron(m1, m2, format="csr")
        new_bool_decomposition[symbol] = new_matrix

    new_automaton = AdjacencyMatrixFA()
    new_automaton.state_to_index = new_state_to_index
    new_automaton.index_to_state = new_index_to_state
    new_automaton.number_of_states = new_number_of_states
    new_automaton.start_states = new_start_states
    new_automaton.final_states = new_final_states
    new_automaton.bool_decomposition = new_bool_decomposition

    return new_automaton


def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    graph_nfa = graph_to_nfa(graph, start_nodes, final_nodes)
    regex_dfa = regex_to_dfa(regex)

    graph_adj = AdjacencyMatrixFA(graph_nfa)
    regex_adj = AdjacencyMatrixFA(regex_dfa)

    intersection_matrix = intersect_automata(graph_adj, regex_adj)
    closure = intersection_matrix.get_transitive_closure()

    result = set()

    for start in intersection_matrix.start_states:
        for final in intersection_matrix.final_states:
            if closure[start, final]:
                graph_start_state = intersection_matrix.index_to_state[start].value[0]
                graph_final_state = intersection_matrix.index_to_state[final].value[0]
                result.add((graph_start_state, graph_final_state))

    return result
