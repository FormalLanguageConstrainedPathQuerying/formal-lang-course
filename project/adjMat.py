from __future__ import annotations
from scipy.sparse import csr_array, kron
from networkx import MultiDiGraph
from pyformlang.finite_automaton import NondeterministicFiniteAutomaton, Symbol
from typing import Dict, Set, Iterable
import numpy as np


class AdjacencyMatrixFA:
    def __init__(
        self,
        b_mats: Dict[Symbol, csr_array],
        start_states: Set[int],
        final_states: Set[int],
    ):
        self.b_mats = b_mats
        self.start_states = start_states
        self.final_states = final_states
        self.mat_size = 0 if not b_mats else ((list(b_mats.values()))[0].shape)[0]

    def from_nfa(nfa: NondeterministicFiniteAutomaton) -> AdjacencyMatrixFA:
        dems = len(nfa.states)
        ids = dict()
        drafts = dict()
        pos = 0
        for st in nfa.states:
            ids[st.value] = pos
            pos = pos + 1
        for st1, sy, st2 in nfa:
            if drafts.get(sy) is None:
                drafts[sy] = ([1], [ids[st1.value]], [ids[st2.value]])
            else:
                data, row_ind, col_ind = drafts.get(sy)
                data.append(1)
                row_ind.append((ids[st1.value]))
                col_ind.append((ids[st2.value]))
        b_mats = {
            sy: csr_array((data, (row_ind, col_ind)), shape=(dems, dems))
            for (sy, (data, row_ind, col_ind)) in drafts.items()
        }
        final_states = [ids[fs.value] for fs in nfa.final_states]
        start_states = [ids[ss.value] for ss in nfa.start_states]
        return AdjacencyMatrixFA(b_mats, start_states, final_states)

    def accepts(self, word: Iterable[Symbol]) -> bool:
        transparents = {sy: m.copy().transpose() for (sy, m) in self.b_mats.items()}
        fr = np.array(
            [1 if st in self.start_states else 0 for st in range(0, self.mat_size)]
        )
        for sy in word:
            if transparents[sy] is None:
                return False
            fr = transparents[sy] @ fr
            if not np.any(fr):
                return False
        for fs in self.final_states:
            if fr[fs] != 0:
                return True
        return False

    def trans_closure(self) -> csr_array:
        acc: csr_array = csr_array(([], ([], [])), shape=(self.mat_size, self.mat_size))
        acc.setdiag(np.ones(self.mat_size))
        for mat in self.b_mats.values():
            acc = acc.maximum(mat)
        prev_nonzero_count = acc.count_nonzero()
        while True:
            acc = acc * acc
            new_nonzero_count = acc.count_nonzero()
            if new_nonzero_count == prev_nonzero_count:
                return acc
            else:
                prev_nonzero_count = new_nonzero_count

    def empty(self) -> bool:
        fr = np.array(
            [1 if st in self.start_states else 0 for st in range(0, self.mat_size)]
        )
        pos_fins = self.trans_closure().transpose() @ fr
        for fs in self.final_states:
            if pos_fins[fs] != 0:
                return False
        return True


def intersect_automata(
    automaton1: AdjacencyMatrixFA, automaton2: AdjacencyMatrixFA
) -> AdjacencyMatrixFA:
    size1 = automaton1.mat_size
    start_states = [
        st1 * size1 + st2
        for st1 in automaton1.start_states
        for st2 in automaton2.start_states
    ]
    final_states = [
        st1 * size1 + st2
        for st1 in automaton1.final_states
        for st2 in automaton2.final_states
    ]
    b_mats = automaton2.b_mats.copy()
    for sy, m1 in automaton1.b_mats.items():
        if automaton2.b_mats[sy] is None:
            b_mats[sy] = m1
        b_mats[sy] = kron(m1, automaton2.b_mats[sy])

    return AdjacencyMatrixFA(b_mats, start_states, final_states)


# fake
def tensor_based_rpq(
    regex: str, graph: MultiDiGraph, start_nodes: set[int], final_nodes: set[int]
) -> set[tuple[int, int]]:
    return set()
