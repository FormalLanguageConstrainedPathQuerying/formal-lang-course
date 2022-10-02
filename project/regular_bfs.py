from copy import copy

import numpy as np
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
from scipy.sparse import lil_matrix, spmatrix, csr_matrix, identity, vstack

from project.automata_utils import from_regex_to_dfa
from project.boolean_decomposition import boolean_decompose_enfa, BooleanDecomposition
from project.graph_utils import from_graph_to_nfa

__all__ = ["regular_bfs"]


class LeftRightMatrix:
    """
    Class representing matrix which was constructed as concatenation of two matrix. These class must be used only inside
    regular_bfs() function.
    """

    def __init__(self, left_submatrix: spmatrix, right_submatrix: spmatrix):
        """
        :param left_submatrix: matrix which will be accessible as left_submatrix()
        :param right_submatrix: matrix which will be accessible as rigt_submatrix(). Height of right_submatrix must be
            same with left_submatrix
        """
        height_left, _ = left_submatrix.get_shape()
        height_right, _ = right_submatrix.get_shape()
        assert height_right == height_left
        self._left_submatrix = left_submatrix
        self._right_submatrix = right_submatrix

    def __copy__(self):
        return LeftRightMatrix(
            self._left_submatrix.copy(), self._right_submatrix.copy()
        )

    def __eq__(self, other):
        if not isinstance(other, LeftRightMatrix):
            return False
        nonzero_self = set(zip(*self._left_submatrix.nonzero())).union(
            set(zip(*self._right_submatrix.nonzero()))
        )
        nonzero_other = set(zip(*other._left_submatrix.nonzero())).union(
            set(zip(*other._right_submatrix.nonzero()))
        )
        return nonzero_self == nonzero_other

    def left_submatrix(self) -> spmatrix:
        return self._left_submatrix

    def right_submatrix(self) -> spmatrix:
        return self._right_submatrix

    def tocsr(self):
        _, width_left = self._left_submatrix.get_shape()
        height_right, width_right = self._right_submatrix.get_shape()
        left_submatrix = self._left_submatrix.tocsr()
        right_submatrix = self._right_submatrix.tocsr()
        data = [left_submatrix[i, j] for (i, j) in zip(*left_submatrix.nonzero())] + [
            right_submatrix[i, j] for (i, j) in zip(*right_submatrix.nonzero())
        ]
        row = [i for (i, _) in zip(*left_submatrix.nonzero())] + [
            i for (i, _) in zip(*right_submatrix.nonzero())
        ]
        col = [j for (_, j) in zip(*left_submatrix.nonzero())] + [
            width_left + j for (_, j) in zip(*right_submatrix.nonzero())
        ]
        return csr_matrix(
            (data, (row, col)), shape=(height_right, width_right + width_left)
        )

    def exclude_visited(self, visited: "LeftRightMatrix"):
        assert (
            self._left_submatrix.get_shape() == visited.left_submatrix().get_shape()
            and self._right_submatrix.get_shape()
            == visited.right_submatrix().get_shape()
        )
        visited_right_submatrix = visited.right_submatrix()
        for (i, j) in zip(*self._right_submatrix.nonzero()):
            if visited_right_submatrix[i, j] != 0:
                self._right_submatrix[i, j] = 0

    def merge(self, other: "LeftRightMatrix", merge_factor: int):
        assert (
            self._left_submatrix.get_shape() == other.left_submatrix().get_shape()
            and self._right_submatrix.get_shape() == other.right_submatrix().get_shape()
        )
        _, width_left = self._left_submatrix.get_shape()
        _, width_right = self._right_submatrix.get_shape()
        for (i, j) in zip(*other.left_submatrix().nonzero()):
            offset = i // merge_factor
            row = other.right_submatrix().getrow(i)
            for (_, k) in zip(*row.nonzero()):
                if row[0, k] != 0:
                    self._right_submatrix[offset * merge_factor + j, k] = 1

    @classmethod
    def vstack(
        cls, matrix1: "LeftRightMatrix", matrix2: "LeftRightMatrix"
    ) -> "LeftRightMatrix":
        return LeftRightMatrix(
            vstack((matrix1.left_submatrix(), matrix2.left_submatrix())).tolil(),
            vstack((matrix1.right_submatrix(), matrix2.right_submatrix())).tolil(),
        )


def from_spmatrix_to_left_right_matrix(
    matrix: spmatrix, width_left: int
) -> LeftRightMatrix:
    height, width = matrix.get_shape()
    assert width > width_left
    matrix = matrix.tocsr()
    left_submatrix = lil_matrix((height, width_left))
    right_submatrix = lil_matrix((height, width - width_left))
    for (i, j) in zip(*matrix.nonzero()):
        if j < width_left:
            left_submatrix[i, j] = matrix[i, j]
        else:
            right_submatrix[i, j - width_left] = matrix[i, j]
    return LeftRightMatrix(left_submatrix, right_submatrix)


def regular_bfs(
    graph_decomposition: BooleanDecomposition,
    regex: Regex,
    separated: bool,
    start_states: list[any] = None,
    final_states: list[any] = None,
) -> set[any] | set[tuple[any, any]]:
    """
    Performs bfs on graph according to restrictions imposed by regex
    :param graph_decomposition: boolean decomposition of graph
    :param regex: regular path constraints in a graph
    :param separated: if true result will be presented as set of 2-element tuples of graph nodes which may be connected
        by path, otherwise result will be presented as set of graph nodes which may be obtained from start_states
    :param start_states: start nodes inside graph (all nodes in None)
    :param final_states: final nodes inside graph (all nodes in None)
    :return: if separated = True result will be presented as set of 2-element tuples of graph nodes which may
        be connected by path, otherwise result will be presented as set of graph nodes which may be obtained
        from start_states
    """
    regex_as_enfa = from_regex_to_dfa(regex)
    regex_decomposition = boolean_decompose_enfa(regex_as_enfa)

    direct_sum_decomposition = regex_decomposition.direct_sum(graph_decomposition)
    regex_states_count = regex_decomposition.states_count()
    graph_states_count = graph_decomposition.states_count()
    if not separated:
        visited = LeftRightMatrix(
            identity(regex_states_count),
            lil_matrix((regex_states_count, graph_states_count)),
        )
        frontier = copy(visited)
        for state in start_states:
            frontier.right_submatrix()[
                regex_decomposition.state_index(regex_as_enfa.start_state),
                graph_decomposition.state_index(state),
            ] = 1
    else:
        visited = LeftRightMatrix(
            identity(regex_states_count),
            lil_matrix((regex_states_count, graph_states_count)),
        )
        for _ in range(len(start_states) - 1):
            visited = LeftRightMatrix.vstack(
                visited,
                LeftRightMatrix(
                    identity(regex_states_count),
                    lil_matrix((regex_states_count, graph_states_count)),
                ),
            )
        frontier = copy(visited)
        for i in range(len(start_states)):
            state = start_states[i]
            frontier.right_submatrix()[
                regex_decomposition.state_index(regex_as_enfa.start_state)
                + i * regex_states_count,
                graph_decomposition.state_index(state),
            ] = 1

    while True:
        last_iteration_visited = copy(visited)
        frontier.exclude_visited(visited)
        new_frontier = copy(frontier)
        for matrix in direct_sum_decomposition.to_dict().values():
            next_step = from_spmatrix_to_left_right_matrix(
                frontier.tocsr() @ matrix.tocsr(), regex_states_count
            )
            new_frontier.merge(next_step, regex_states_count)
        visited.merge(frontier, regex_states_count)
        frontier = new_frontier

        if last_iteration_visited.tocsr().nnz == visited.tocsr().nnz:
            break

    result = set()
    if not separated:
        for final_regex in regex_as_enfa.final_states:
            row = visited.right_submatrix().getrow(
                regex_decomposition.state_index(final_regex)
            )
            for (_, j) in zip(*row.nonzero()):
                state = graph_decomposition.states()[j].value
                if state not in start_states and state in final_states:
                    result.add(state)
    else:
        for i in range(len(start_states)):
            subresult = set()
            for final_regex in regex_as_enfa.final_states:
                offset = i * regex_states_count
                row = visited.right_submatrix().getrow(
                    offset + regex_decomposition.state_index(final_regex)
                )
                for (_, j) in zip(*row.nonzero()):
                    state = graph_decomposition.states()[j].value
                    if state not in start_states and state in final_states:
                        subresult.add((start_states[i], state))
            result = result.union(subresult)

    return result


graph = MultiDiGraph()
graph.add_node(0)
graph.add_node(1)
graph.add_node(2)
graph.add_edge(0, 1, label="a")
graph.add_edge(1, 2, label="e")
graph.add_edge(0, 2, label="c")
print(
    regular_bfs(
        boolean_decompose_enfa(from_graph_to_nfa(graph)),
        Regex("c|e"),
        True,
        [0, 1],
        [2],
    )
)
