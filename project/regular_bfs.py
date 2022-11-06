from copy import copy

from pyformlang.finite_automaton import State
from pyformlang.regular_expression import Regex
from scipy.sparse import lil_matrix, spmatrix, identity

from project.automata_utils import from_regex_to_dfa
from project.boolean_decomposition import boolean_decompose_enfa, BooleanDecomposition

__all__ = ["regular_bfs"]

from project.left_right_matrix import LeftRightMatrix


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
    start_states: list[any],
) -> set[State] | set[tuple[State, State]]:
    """
    Performs bfs on graph according to restrictions imposed by regex
    :param graph_decomposition: boolean decomposition of graph
    :param regex: regular path constraints in a graph
    :param separated: if true result will be presented as set of 2-element tuples of graph nodes which may be connected
        by path, otherwise result will be presented as set of graph nodes which may be obtained from start_states
    :param start_states: start nodes inside graph
    :return: if separated = True result will be presented as set of 2-element tuples of graph nodes which may
        be connected by path, otherwise result will be presented as set of graph nodes which may be obtained
        from start_states
    """
    regex_as_enfa = from_regex_to_dfa(regex)
    regex_decomposition = boolean_decompose_enfa(regex_as_enfa)

    direct_sum_decomposition = regex_decomposition.direct_sum(graph_decomposition)
    direct_sum_decomposition_as_matrices = direct_sum_decomposition.to_dict().values()
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

    last_iteration_visited = copy(visited.tospmatrix())
    while True:
        frontier.exclude_visited(visited)
        frontier_as_spmatrix = frontier.tospmatrix()
        new_frontier = copy(frontier)
        for matrix in direct_sum_decomposition_as_matrices:
            next_step = from_spmatrix_to_left_right_matrix(
                frontier_as_spmatrix @ matrix, regex_states_count
            )
            new_frontier.merge(next_step, regex_states_count)
        visited.merge(frontier, regex_states_count)
        frontier = new_frontier

        visited_as_spmatrix = visited.tospmatrix()
        if last_iteration_visited.nnz == visited_as_spmatrix.nnz:
            break
        else:
            last_iteration_visited = visited_as_spmatrix

    result = set()
    if not separated:
        for final_regex in regex_as_enfa.final_states:
            row = visited.right_submatrix().getrow(
                regex_decomposition.state_index(final_regex)
            )
            for (_, j) in zip(*row.nonzero()):
                state = (graph_decomposition.states())[j]
                if state.value not in start_states:
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
                    state = (graph_decomposition.states())[j]
                    if state.value != start_states[i]:
                        subresult.add((State(start_states[i]), state))
            result = result.union(subresult)

    return result
