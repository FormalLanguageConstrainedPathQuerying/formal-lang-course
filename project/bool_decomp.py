from pyformlang.finite_automaton import EpsilonNFA
from scipy.sparse import csr_array, dok_array, lil_array, kron, bmat, vstack
from itertools import product
from typing import Any, NamedTuple

from project.rsm import RSM


class BoolDecomp:
    class StateInfo(NamedTuple):
        data: Any
        is_start: bool
        is_final: bool

        def __eq__(self, other):
            return isinstance(other, BoolDecomp.StateInfo) and self.data == other.data

        def __hash__(self):
            return hash(self.data)

    def __init__(
        self,
        states: list[StateInfo] | None = None,
        adjs: dict[Any, csr_array] | None = None,
    ):
        self.states: list[BoolDecomp.StateInfo] = states if states is not None else []
        self.adjs: dict[Any, csr_array] = adjs if adjs is not None else {}

    @classmethod
    def from_nfa(cls, nfa: EpsilonNFA, sort_states: bool = False) -> "BoolDecomp":
        states = list(
            {
                cls.StateInfo(
                    data=st.value,
                    is_start=st in nfa.start_states,
                    is_final=st in nfa.final_states,
                )
                for st in nfa.states
            }
        )
        if sort_states:
            states.sort(key=lambda st: st.data)

        adjs = {}
        transitions = nfa.to_dict()
        for n_from in transitions:
            for symbol, ns_to in transitions[n_from].items():
                adj = adjs.setdefault(
                    symbol.value, dok_array((len(states), len(states)), dtype=bool)
                )
                start_index = next(i for i, s in enumerate(states) if s.data == n_from)
                for n_to in ns_to if isinstance(ns_to, set) else {ns_to}:
                    end_index = next(i for i, s in enumerate(states) if s.data == n_to)
                    adj[start_index, end_index] = True
        for key in adjs:
            adjs[key] = adjs[key].tocsr()

        return cls(states, adjs)

    @classmethod
    def from_rsm(cls, rsm: RSM, sort_states: bool = False) -> "BoolDecomp":
        states = list(
            {
                cls.StateInfo(
                    data=(var, st.value),
                    is_start=st in nfa.start_states,
                    is_final=st in nfa.final_states,
                )
                for var, nfa in rsm.boxes.items()
                for st in nfa.states
            }
        )
        if sort_states:
            states.sort(key=lambda st: (st.data[0].value, st.data[1]))

        adjs = {}
        for var, nfa in rsm.boxes.items():
            transitions = nfa.to_dict()
            for n_from in transitions:
                for symbol, ns_to in transitions[n_from].items():
                    adj = adjs.setdefault(
                        symbol.value, dok_array((len(states), len(states)), dtype=bool)
                    )
                    start_index = next(
                        i for i, s in enumerate(states) if s.data == (var, n_from)
                    )
                    for n_to in ns_to if isinstance(ns_to, set) else {ns_to}:
                        end_index = next(
                            i for i, s in enumerate(states) if s.data == (var, n_to)
                        )
                        adj[start_index, end_index] = True
        for key in adjs:
            adjs[key] = adjs[key].tocsr()

        return cls(states, adjs)

    def intersect(self, other: "BoolDecomp") -> "BoolDecomp":
        states = [
            self.StateInfo(
                data=(st1.data, st2.data),
                is_start=st1.is_start and st2.is_start,
                is_final=st1.is_final and st2.is_final,
            )
            for st1, st2 in product(self.states, other.states)
        ]

        adjs = {}
        n = len(states)
        for symbol in set(self.adjs.keys()).union(set(other.adjs.keys())):
            if symbol in self.adjs and symbol in other.adjs:
                adjs[symbol] = csr_array(
                    kron(self.adjs[symbol], other.adjs[symbol], format="csr")
                )
            else:
                adjs[symbol] = csr_array((n, n), dtype=bool)

        return BoolDecomp(states, adjs)

    def transitive_closure_any_symbol(self) -> tuple[list[int], list[int]]:
        n = len(self.states)
        adj_all = sum(self.adjs.values(), start=csr_array((n, n), dtype=bool))
        adj_all.eliminate_zeros()

        while True:
            prev_path_num = adj_all.nnz
            adj_all += adj_all @ adj_all
            if prev_path_num == adj_all.nnz:
                break

        return adj_all.nonzero()

    def _direct_sum(self, other: "BoolDecomp") -> "BoolDecomp":
        states = self.states + other.states

        adjs = {}
        for symbol in set(self.adjs.keys()).intersection(set(other.adjs.keys())):
            adjs[symbol] = csr_array(
                bmat([[self.adjs[symbol], None], [None, other.adjs[symbol]]])
            )

        return BoolDecomp(states, adjs)

    def constrained_bfs(
        self, constraint: "BoolDecomp", separated: bool = False
    ) -> set[int] | set[tuple[int, int]]:
        n = len(constraint.states)

        direct_sum = constraint._direct_sum(self)

        start_states_indices = [i for i, st in enumerate(self.states) if st.is_start]
        init_front = (
            _init_bfs_front(self.states, constraint.states)
            if not separated
            else _init_separated_bfs_front(
                self.states, constraint.states, start_states_indices
            )
        )

        visited = csr_array(init_front.shape, dtype=bool)

        while True:
            old_visited_nnz = visited.nnz

            for _, adj in direct_sum.adjs.items():
                front_part = visited @ adj if init_front is None else init_front @ adj
                visited += _transform_front_part(front_part, n)

            init_front = None

            if visited.nnz == old_visited_nnz:
                break

        results = set()
        for i, j in zip(*visited.nonzero()):
            if j >= n and constraint.states[i % n].is_final:
                self_st_index = j - n
                if self.states[self_st_index].is_final:
                    results.add(
                        self_st_index
                        if not separated
                        else (start_states_indices[i // n], self_st_index)
                    )
        return results


def _transform_front_part(front_part: csr_array, constr_states_num: int) -> csr_array:
    transformed_front_part = lil_array(front_part.shape, dtype=bool)
    for i, j in zip(*front_part.nonzero()):
        if j < constr_states_num:
            non_zero_row_right = front_part.getrow(i).tolil()[[0], constr_states_num:]
            if non_zero_row_right.nnz > 0:
                row_shift = i // constr_states_num * constr_states_num
                transformed_front_part[row_shift + j, j] = True
                transformed_front_part[
                    [row_shift + j], constr_states_num:
                ] += non_zero_row_right
    return transformed_front_part.tocsr()


def _init_bfs_front(
    self_states: list[BoolDecomp.StateInfo],
    constr_states: list[BoolDecomp.StateInfo],
    self_start_row: lil_array | None = None,
) -> csr_array:
    front = lil_array(
        (len(constr_states), len(constr_states) + len(self_states)), dtype=bool
    )

    if self_start_row is None:
        self_start_row = lil_array([st.is_start for st in self_states], dtype=bool)

    for i, st in enumerate(constr_states):
        if st.is_start:
            front[i, i] = True
            front[i, len(constr_states) :] = self_start_row

    return front.tocsr()


def _init_separated_bfs_front(
    self_states: list[BoolDecomp.StateInfo],
    constr_states: list[BoolDecomp.StateInfo],
    start_states_indices: list[int],
) -> csr_array:
    fronts = [
        _init_bfs_front(
            self_states,
            constr_states,
            self_start_row=lil_array(
                [i == st_i for i in range(len(self_states))], dtype=bool
            ),
        )
        for st_i in start_states_indices
    ]
    return (
        csr_array(vstack(fronts))
        if len(fronts) > 0
        else csr_array(
            (len(constr_states), len(constr_states) + len(self_states)), dtype=bool
        )
    )
