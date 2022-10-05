from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex

from project.boolean_decompositon import BooleanDecomposition
from project.regex_utils import create_nfa_from_graph, regex_to_dfa
from scipy.sparse import block_diag, csr_matrix, vstack
from pyformlang.finite_automaton import State


def rpq_bfs(
    graph: MultiDiGraph,
    regex: Regex,
    start_states: set[int] = None,
    final_states: set[int] = None,
    is_for_each: bool = False,
) -> set:
    graph_bool_decomposition = BooleanDecomposition(
        create_nfa_from_graph(graph, start_states, final_states)
    )
    regex_bool_decomposition = BooleanDecomposition(regex_to_dfa(regex))

    return bfs_sync(graph_bool_decomposition, regex_bool_decomposition, is_for_each)


def get_reachable_nodes(regex, graph, front, direct_sum, is_for_each):
    visited = csr_matrix(front.shape, dtype=bool)
    is_first_step = True
    while True:
        old_visited_nnz = visited.nnz
        for mtx in direct_sum.values():
            step = front @ mtx if is_first_step else visited @ mtx
            visited += transform_rows(step, regex.states_num, is_for_each)

        is_first_step = False

        if old_visited_nnz == visited.nnz:
            break

    reachable_nodes_acc = set()
    regex_states = list(regex.state_indices.keys())
    graph_states = list(graph.state_indices.keys())
    for row, col in zip(*visited.nonzero()):
        if (
            not col < regex.states_num
            and regex_states[row % regex.states_num] in regex.final_states
        ):
            state_index = col - regex.states_num
            if graph_states[state_index] in graph.final_states:
                if is_for_each:
                    reachable_nodes_acc.add(
                        (State(row // regex.states_num), State(state_index))
                    )
                else:
                    reachable_nodes_acc.add(State(state_index))

    return reachable_nodes_acc


def bfs_sync(
    graph: BooleanDecomposition, regex: BooleanDecomposition, is_for_each: bool = False
) -> set:
    if len(graph.state_indices.keys()) == 0 or len(regex.state_indices.keys()) == 0:
        return set()

    direct_sum = {}
    for label in graph.bool_decomposition.keys() & regex.bool_decomposition.keys():
        direct_sum[label] = block_diag(
            (regex.bool_decomposition[label], graph.bool_decomposition[label])
        )

    front = (
        vstack([create_front(graph, regex, {st}) for st in graph.get_start_states()])
        if is_for_each
        else create_front(graph, regex, graph.get_start_states())
    )

    return get_reachable_nodes(regex, graph, front, direct_sum, is_for_each)


def create_front(
    graph: BooleanDecomposition, regex: BooleanDecomposition, start_states
) -> csr_matrix:
    front = csr_matrix(
        (regex.states_num, regex.states_num + graph.states_num), dtype=bool
    )

    for state in regex.get_start_states():
        i = regex.state_indices[state]
        front[i, i] = True

        for graph_st in start_states:
            front[i, regex.states_num + graph_st.value] = True

    return front


def transform_rows(step: csr_matrix, regex_states, is_for_each) -> csr_matrix:
    result = csr_matrix(step.shape, dtype=bool)

    for row, col in zip(*step.nonzero()):
        if col < regex_states:
            right_row = step[row, regex_states:]
            if right_row.nnz != 0:
                if not is_for_each:
                    result[col, col] = True
                    result[col, regex_states:] += right_row
                else:
                    node_number = row // regex_states
                    result[node_number * regex_states + col, col] = True
                    result[node_number * regex_states + col, regex_states:] += right_row

    return result
