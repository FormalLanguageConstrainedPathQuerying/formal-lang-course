import networkx as nx
from pyformlang.regular_expression import Regex

from project.automata_tools import create_nfa_from_graph, regex_to_minimal_dfa
from project.boolean_matrices import BooleanMatrices
from scipy.sparse import csr_matrix, csr_array, lil_array
from scipy import sparse


def rpq_bfs(
    graph: nx.MultiDiGraph,
    reg_constraint: Regex,
    start_states: set = None,
    final_states: set = None,
    separately_for_each: bool = False,
):
    if len(start_states) == 0 or len(final_states) == 0:
        return set()

    # step-1 form bm
    graph_bm = BooleanMatrices(create_nfa_from_graph(graph, start_states, final_states))
    constraint_bm = BooleanMatrices(regex_to_minimal_dfa(reg_constraint))
    k = constraint_bm.num_states
    n = graph_bm.num_states

    # step-2 apply direct sum
    d_sum = constraint_bm.direct_sum(graph_bm)

    # step-3 form front
    graph_start_states_indexes = [
        graph_bm.state_indexes[start_st] for start_st in graph_bm.start_states
    ]
    if separately_for_each:
        front = _create_front_for_each(
            graph_bm, constraint_bm, graph_start_states_indexes
        )
    else:
        front = _create_front(graph_bm, constraint_bm, graph_start_states_indexes)

    # step-4 while-loop with new_front = front @ d_sum
    # думаю надо копировать в том числе содержимое фронта, а не только его форму
    visited = csr_array(front)

    while True:
        old_visited_nnz = visited.nnz

        for d_sum_bm in d_sum.bool_matrices.values():
            front_part = visited @ d_sum_bm if front is None else front @ d_sum_bm
            # step-5, 6
            visited += _correct_front_part(front_part, k, n)

        front = None

        if visited.nnz == old_visited_nnz:
            break
    # step-7
    result = set()
    for i, j in zip(*visited.nonzero()):
        if j >= k:

            state_constraint = constraint_bm.get_state_by_index(
                i % k
            )  # % для случая separated_for_each

            graph_state_index = j - k
            state_graph = graph_bm.get_state_by_index(graph_state_index)

            if (
                state_constraint in constraint_bm.final_states
                and state_graph in graph_bm.final_states
            ):
                if not separately_for_each:
                    result.add(graph_bm.get_state_by_index(graph_state_index))
                else:
                    result.add(
                        (
                            constraint_bm.get_state_by_index(i // k),
                            graph_bm.get_state_by_index(graph_state_index),
                        )
                    )

    return result


def _correct_front_part(
    front_part: csr_array, constraint_num_states: int, graph_num_states: int
):
    corrected_front_part = lil_array(front_part.shape)

    for i, j in zip(*front_part.nonzero()):
        if j < constraint_num_states:
            row_right_part = front_part.getrow(i).tolil()[[0], constraint_num_states:]
            if row_right_part.nnz > 0:
                row_shift = i // graph_num_states * graph_num_states
                corrected_front_part[row_shift + j, j] = True
                corrected_front_part[
                    row_shift + j, constraint_num_states:
                ] = row_right_part

    return corrected_front_part.tocsr()


def _create_front(
    graph_bm: BooleanMatrices,
    constraint_bm: BooleanMatrices,
    graph_start_states_indexes,
) -> csr_matrix:
    right_part_of_row = sparse.dok_matrix((1, graph_bm.num_states), dtype=bool)

    for i in graph_start_states_indexes:
        right_part_of_row[0, i] = True
    right_part_of_row = right_part_of_row.tocsr()

    front = sparse.csr_matrix(
        (constraint_bm.num_states, constraint_bm.num_states + graph_bm.num_states),
        dtype=bool,
    )

    for start_st in constraint_bm.start_states:
        i = constraint_bm.state_indexes[start_st]
        front[i, i] = True
        front[i, constraint_bm.num_states :] = right_part_of_row

    return front


def _create_front_for_each(
    graph_bm: BooleanMatrices,
    constraint_bm: BooleanMatrices,
    graph_start_states_indexes,
):
    front = sparse.vstack(
        [
            _create_front(graph_bm, constraint_bm, {i})
            for i in graph_start_states_indexes
        ]
    )

    return front
