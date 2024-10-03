from collections import defaultdict
from dataclasses import dataclass
from functools import reduce
import itertools
import operator
from typing import Any, Dict, Iterable, Optional, Self, TypeAlias
from networkx.classes.multidigraph import MultiDiGraph
import numpy as np
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton
from pyformlang.finite_automaton.state import State
from pyformlang.finite_automaton.symbol import Symbol
from scipy.sparse._csr import csr_matrix
from scipy.sparse import kron

from project.task2 import graph_to_nfa, regex_to_dfa

Transition: TypeAlias = Any


@dataclass
class AdjacencyMatrixFA:
    start_states: set
    final_states: set
    adjacency_matrixes_boolean_decomposition: dict[Transition, csr_matrix]
    index_of_states: dict[State, int]

    @property
    def state_count(self):
        return len(self.index_of_states)

    @property
    def states(self):
        return self.index_of_states.keys()

    @property
    def state_of_indexes(self):
        return {idx: state for state, idx in self.index_of_states.items()}

    def __init__(self, automaton: Optional[NondeterministicFiniteAutomaton]):
        if automaton is None:
            return
        graph = automaton.to_networkx()
        self.index_of_states = {state: idx for idx, state in enumerate(graph.nodes)}
        self.start_states = set()
        self.final_states = set()
        for node, data in graph.nodes(data=True):
            if data.get("is_start"):
                self.start_states.add(node)
            if data.get("is_final"):
                self.final_states.add(node)

        state_count = len(self.index_of_states)
        adjacency_matrixes_boolean_decomposition: Dict[Transition, list[list[bool]]] = (
            defaultdict(
                lambda: np.zeros(shape=(state_count, state_count), dtype=np.bool_)
            )
        )
        for state, destination_state, transition in graph.edges(data="label"):
            if transition:
                adjacency_matrixes_boolean_decomposition[transition][
                    self.index_of_states[state],
                    self.index_of_states[destination_state],
                ] = True
        self.adjacency_matrixes_boolean_decomposition = {
            transition: csr_matrix(adjacency_matrix)
            for transition, adjacency_matrix in adjacency_matrixes_boolean_decomposition.items()
        }

    def accepts(self, word: Iterable[Symbol]) -> bool:
        @dataclass
        class ToCheck:
            symbols: Iterable[Symbol]
            state: int

        queue = [
            ToCheck(symbols=word, state=self.index_of_states[start_state])
            for start_state in self.start_states
        ]
        final_states_indexes = set(
            self.index_of_states[state] for state in self.final_states
        )
        while queue:
            to_check = queue.pop(0)
            symbols = to_check.symbols
            try:
                symbol = next(symbols)
            except StopIteration:
                if to_check.state in final_states_indexes:
                    return True
                continue
            adjacency_matrix_of_symbol = (
                self.adjacency_matrixes_boolean_decomposition.get(symbol)
            )
            if adjacency_matrix_of_symbol is None:
                continue
            for state in adjacency_matrix_of_symbol[to_check.state].indices:
                queue.append(ToCheck(symbols=iter(symbols), state=state))
        return False

    def transitive_closure(self) -> csr_matrix:
        adjacency_matrixes = list(
            self.adjacency_matrixes_boolean_decomposition.values()
        )
        if adjacency_matrixes:
            if len(adjacency_matrixes) > 1:
                transitions: csr_matrix = reduce(
                    operator.add, adjacency_matrixes[1:], adjacency_matrixes[0]
                )
            else:
                transitions: csr_matrix = adjacency_matrixes[0]
        else:
            return csr_matrix(np.eye(self.state_count, dtype=np.bool_))
        transitions.setdiag(True)
        res: csr_matrix = transitions.copy()
        for _ in range(2, self.state_count + 1):
            new_res = res * transitions
            if np.array_equal(res.todense(), new_res.todense()):
                break
            else:
                res = new_res
        return res

    def is_empty(self) -> bool:
        trans_closure = self.transitive_closure()
        for i, row in enumerate(trans_closure):
            for j in row.indices:
                if i in self.start_states and j in self.final_states:
                    return False
        return True

    @classmethod
    def intersect_automata(cls, automaton1: Self, automaton2: Self) -> Self:
        inst = cls(None)
        state_count = automaton1.state_count * automaton2.state_count

        def get_new_state_index(state1, state2):
            return (
                automaton1.index_of_states[state1] * automaton2.state_count
                + automaton2.index_of_states[state2]
            )

        def iter_and_add(automaton_attr: str):
            return set(
                (automaton1_state, automaton2_state)
                for automaton1_state in getattr(automaton1, automaton_attr)
                for automaton2_state in getattr(automaton2, automaton_attr)
            )

        inst.start_states = iter_and_add("start_states")
        inst.final_states = iter_and_add("final_states")

        adjacency_matrixes_boolean_decomposition: Dict[Transition, list[list[bool]]] = (
            defaultdict(
                lambda: np.zeros(
                    shape=(state_count, state_count),
                    dtype=np.bool_,
                )
            )
        )

        for (
            trans1,
            bool_adj1,
        ) in automaton1.adjacency_matrixes_boolean_decomposition.items():
            for (
                trans2,
                bool_adj2,
            ) in automaton2.adjacency_matrixes_boolean_decomposition.items():
                if trans1 == trans2:
                    adjacency_matrixes_boolean_decomposition[trans1] = kron(
                        bool_adj1, bool_adj2, "csr"
                    )
        inst.adjacency_matrixes_boolean_decomposition = (
            adjacency_matrixes_boolean_decomposition
        )
        inst.index_of_states = {
            (state1, state2): get_new_state_index(state1, state2)
            for state1 in automaton1.states
            for state2 in automaton2.states
        }
        return inst


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    return AdjacencyMatrixFA.intersect_automata(automaton1, automaton2)


def tensor_based_rpq(
    regex: str,
    graph: MultiDiGraph,
    start_nodes: set[int],
    final_nodes: set[int],
) -> set[tuple[int, int]]:
    adj_from_regex = AdjacencyMatrixFA(regex_to_dfa(regex))
    adj_from_graph = AdjacencyMatrixFA(graph_to_nfa(graph, start_nodes, final_nodes))
    intersected = intersect_automata(adj_from_graph, adj_from_regex)

    trans_closure = intersected.transitive_closure()
    res = set()
    for (start_state_graph, start_state_regex), (
        final_state_graph,
        final_state_regex,
    ) in itertools.product(intersected.start_states, intersected.final_states):
        if trans_closure[
            intersected.index_of_states[(start_state_graph, start_state_regex)],
            intersected.index_of_states[(final_state_graph, final_state_regex)],
        ]:
            res.add((start_state_graph, final_state_graph))

    return res
