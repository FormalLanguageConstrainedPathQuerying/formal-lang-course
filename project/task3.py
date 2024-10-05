from itertools import product
from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol
from functools import reduce
from typing import Iterable
from scipy.sparse import csr_matrix, kron

from project.task2_fa import regex_to_dfa, graph_to_nfa


class AdjacencyMatrixFA:
    def __init__(self, fa: NondeterministicFiniteAutomaton):
        self.states = {st: i for (i, st) in enumerate(fa.states)}
        self.start_states = set(self.states[st] for st in fa.start_states)
        self.final_states = set(self.states[st] for st in fa.final_states)
        self.number_of_states = len(self.states)

        self.adj_matrix = {}
        for sym in fa.symbols:
            self.adj_matrix[sym] = csr_matrix((self.number_of_states, self.number_of_states), dtype=bool)

        graph = fa.to_networkx()

        for u, v, label in graph.edges(data="label"):
            if label:
                self.adj_matrix[label][self.states[u], self.states[v]] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        symbols = list(word)
        configs = [(st, symbols) for st in self.start_states]

        while len(configs) > 0:
            state, rest = configs.pop()
            if not rest:
                if state in self.final_states:
                    return True
                continue

            for next_state in range(self.number_of_states):
                if self.adj_matrix[rest[0]][state, next_state]:
                    configs.append((next_state, rest[1:]))
        return False

    def transitive_closure(self):
        init_matrix = csr_matrix((self.number_of_states, self.number_of_states), dtype=bool)
        init_matrix.setdiag(True)

        if not self.adj_matrix:
            return init_matrix

        reach: csr_matrix = init_matrix + reduce(
            lambda x, y: x + y, self.adj_matrix.values()
        )

        for k in range(self.number_of_states):
            for i in range(self.number_of_states):
                for j in range(self.number_of_states):
                    reach[i, j] = reach[i, j] or (reach[i, k] and reach[k, j])

        return reach

    def is_empty(self) -> bool:
        tc = self.transitive_closure()
        for start in self.start_states:
            for final in self.final_states:
                if tc[start, final]:
                    return False

        return True


def intersect_automata(
        mfa1: AdjacencyMatrixFA, mfa2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    intersection = AdjacencyMatrixFA(NondeterministicFiniteAutomaton())
    intersection.number_of_states = mfa1.number_of_states * mfa2.number_of_states

    for st1 in mfa1.states:
        for st2 in mfa2.states:
            idx1, idx2 = mfa1.states[st1], mfa2.states[st2]
            intersection_idx = len(mfa2.states) * idx1 + idx2

            if idx1 in mfa1.start_states and idx2 in mfa2.start_states:
                intersection.start_states.add(intersection_idx)
            if idx1 in mfa1.final_states and idx2 in mfa2.final_states:
                intersection.final_states.add(intersection_idx)

            intersection.states[(st1, st2)] = intersection_idx

    for sym, adj1 in mfa1.adj_matrix.items():
        if sym not in mfa2.adj_matrix:
            continue

        adj2 = mfa2.adj_matrix[sym]
        intersection.adj_matrix[sym] = kron(adj1, adj2, format="csr")

    return intersection


def tensor_based_rpq(regex: str, graph: MultiDiGraph, start_nodes: set[int],
                     final_nodes: set[int]) -> set[tuple[int, int]]:
    regex_mfa = AdjacencyMatrixFA(regex_to_dfa(regex))
    graph_mfa = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))
    intersection = intersect_automata(regex_mfa, graph_mfa)
    tc = intersection.transitive_closure()

    result = set()

    for start_graph_state in start_nodes:
        for final_graph_state in final_nodes:
            for start_regex_state in regex_mfa.start_states:
                for final_regex_state in regex_mfa.final_states:
                    start_index = intersection.states[(start_graph_state, start_regex_state)]
                    final_index = intersection.states[(final_graph_state, final_regex_state)]
                    if tc[start_index, final_index]:
                        result.add((start_graph_state, final_graph_state))
    return result