from typing import Union, Iterable

from networkx import MultiDiGraph
from pyformlang.finite_automaton import Symbol

from pyformlang.finite_automaton import DeterministicFiniteAutomaton
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton import State
from pyformlang.finite_automaton import EpsilonNFA
import scipy.sparse as sparse

import project.task2 as task2


def as_set(obj):
    if not isinstance(obj, set):
        return {obj}
    return obj


class FiniteAutomaton:
    def __init__(
        self,
        input_automaton: Union[
            NondeterministicFiniteAutomaton, DeterministicFiniteAutomaton, EpsilonNFA
        ],
    ):
        self.start_states = input_automaton.start_states
        self.final_states = input_automaton.final_states
        self.state_to_idx = {v: i for i, v in enumerate(input_automaton.states)}
        self.matrix = dict()

        states = input_automaton.to_dict()
        len_states = len(input_automaton.states)

        for label in input_automaton.symbols:
            self.matrix[label] = sparse.dok_matrix((len_states, len_states), dtype=bool)
            for u, edges in states.items():
                if label in edges:
                    for v in as_set(edges[label]):
                        self.matrix[label][
                            self.state_to_idx[u], self.state_to_idx[v]
                        ] = True

    def accepts(self, word: Iterable[Symbol]) -> bool:
        return self.to_nda().accepts(word)

    def is_empty(self) -> bool:
        return len(self.matrix) == 0 or len(list(self.matrix.values())[0]) == 0

    def to_nda(self) -> NondeterministicFiniteAutomaton:
        ans = NondeterministicFiniteAutomaton()

        for label in self.matrix.keys():
            matrix_size = self.matrix[label].shape[0]
            for x in range(matrix_size):
                for y in range(matrix_size):
                    if self.matrix[label][x, y]:
                        ans.add_transition(
                            self.state_to_idx[State(x)],
                            label,
                            self.state_to_idx[State(y)],
                        )

        for s in self.start_states:
            ans.add_start_state(self.state_to_idx[State(s)])

        for s in self.final_states:
            ans.add_final_state(self.state_to_idx[State(s)])

        return ans

    def __len__(self):
        return len(self.state_to_idx)


def intersect_automata(
    automaton_1: FiniteAutomaton, automaton_2: FiniteAutomaton
) -> EpsilonNFA:
    number_of_states = len(automaton_2)
    symbols_set = set(automaton_1.matrix.keys()).intersection(automaton_2.matrix.keys())
    matrices = {
        label: sparse.kron(automaton_1.matrix[label], automaton_2.matrix[label])
        for label in symbols_set
    }

    result_automaton = EpsilonNFA()

    for symbol, mat in matrices.items():
        from_idx, to_idx = mat.nonzero()
        for _from, _to in zip(from_idx, to_idx):
            result_automaton.add_transition(_from, symbol, _to)

    for s1 in automaton_1.start_states:
        for s2 in automaton_2.start_states:
            result_automaton.add_start_state(
                automaton_1.state_to_idx[s1] * number_of_states
                + automaton_2.state_to_idx[s2]
            )

    for s1 in automaton_1.final_states:
        for s2 in automaton_2.final_states:
            result_automaton.add_final_state(
                automaton_1.state_to_idx[s1] * number_of_states
                + automaton_2.state_to_idx[s2]
            )

    return result_automaton


def paths_ends(
    graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int], regex: str
):
    query = task2.regex_to_dfa(regex)
    aut = task2.graph_to_nfa(graph, start_nodes, final_nodes)

    both = FiniteAutomaton(intersect_automata(query, aut))
    flat = None
    for mat in both.matrix.values():
        if flat is None:
            flat = mat
            continue
        flat |= mat
    if flat is None:
        return []

    prev = 0
    while flat.count_nonzero() != prev:
        prev = flat.count_nonzero()
        flat += flat @ flat

    rev_idx = {i: k for k, i in both.state_to_idx.items()}
    names = list(aut.states)
    n_states = len(names)
    result = set()

    from_idx, to_idx = flat.nonzero()
    for fro, to in zip(from_idx, to_idx):
        fro_id = rev_idx[fro]
        to_id = rev_idx[to]
        if fro_id in both.start_states and to_id in both.final_states:
            result.add((names[fro_id.value % n_states], names[to_id.value % n_states]))

    return list(result)
