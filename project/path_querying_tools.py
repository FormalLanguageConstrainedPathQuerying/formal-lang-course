from typing import Set, Tuple

import networkx as nx
from pyformlang.cfg import CFG, Variable
from pyformlang.regular_expression import Regex
from scipy import sparse

from project.automaton_tools import get_min_dfa_from_regex, get_nfa_from_graph
from project.grammar_tools import hellings, get_wcnf_from_cfg
from project.matrix_tools import BooleanAdjacencies

__all__ = [
    "regular_path_querying",
    "regular_str_path_querying",
    "hellings_context_free_path_querying",
    "matrix_context_free_path_querying",
]


def regular_str_path_querying(
    graph: nx.MultiDiGraph,
    query_str: str,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Using the specified graph and a regular string query,
    finds all pairs of reachable node numbers.

    If start_nodes or final_nodes are not specified,
    all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    query_str: str
        Query to graph as a string
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers

    Raises
    ------
    ValueError
        If non-existent in the specified graph node number is used
    MisformedRegexError
        If specified regex_str has an irregular format
    """

    return regular_path_querying(
        graph, Regex(query_str), start_node_nums, final_node_nums
    )


def regular_path_querying(
    graph: nx.MultiDiGraph,
    query_regex: Regex,
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Using the specified graph and a regular expression query,
    finds all pairs of reachable node numbers.

    If start_nodes or final_nodes are not specified,
    all nodes are considered start or final respectively.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    query_regex: Regex
        Query to graph as complete Regex
    start_node_nums: Set[int], default = None
        Set of start node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers to configure Nondeterministic Finite Automaton,
        which must exist in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers

    Raises
    ------
    ValueError
        If non-existent in the specified graph node number is used
    """

    graph = BooleanAdjacencies(
        get_nfa_from_graph(graph, start_node_nums, final_node_nums)
    )

    query = BooleanAdjacencies(get_min_dfa_from_regex(query_regex))

    intersection = graph.intersect(query)
    transitive_closure = intersection.get_transitive_closure()

    reachable_state_nums = set()

    for state_from_num, state_to_num in zip(*transitive_closure.nonzero()):
        state_from = intersection.nums_states[state_from_num]
        state_to = intersection.nums_states[state_to_num]

        if (
            state_from in intersection.start_states
            and state_to in intersection.final_states
        ):
            reachable_state_from_num = state_from_num // query.states_num
            reachable_state_to_num = state_to_num // query.states_num

            reachable_state_nums.add((reachable_state_from_num, reachable_state_to_num))

    return reachable_state_nums


def hellings_context_free_path_querying(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_symbol: str = "S",
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Context Free Path Querying based on Hellings.

    Using the specified graph, context free query and parameters
    finds all pairs of reachable node numbers.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    cfg: CFG
         Query to graph as context free grammar
    start_symbol: str, default = 'S'
        Start symbol for context free grammar
    start_node_nums: Set[int], default = None
        Set of start node numbers in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers
    """

    cfg._start_symbol = Variable(start_symbol)

    reachable_node_nums = {
        (node_num_l, node_num_r)
        for node_num_l, head, node_num_r in hellings(graph, cfg)
        if head == cfg.start_symbol
    }

    if start_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_l in start_node_nums
        }

    if start_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_r in final_node_nums
        }

    return reachable_node_nums


def matrix_context_free_path_querying(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_symbol: str = "S",
    start_node_nums: Set[int] = None,
    final_node_nums: Set[int] = None,
) -> Set[Tuple[int, int]]:
    """
    Context Free Path Querying based on boolean matrices multiplication.

    Using the specified graph, context free query and parameters
    finds all pairs of reachable node numbers.

    Parameters
    ----------
    graph: nx.MultiDiGraph
        Graph for queries
    cfg: CFG
        Query to graph as context free grammar
    start_symbol: str, default = 'S'
        Start symbol for context free grammar
    start_node_nums: Set[int], default = None
        Set of start node numbers in the graph
    final_node_nums: Set[int], default = None
        Set of final node numbers in the graph

    Returns
    -------
    Set[Tuple[int, int]]
        Set of all pairs of reachable node numbers
    """

    cfg._start_symbol = Variable(start_symbol)
    wcnf = get_wcnf_from_cfg(cfg)

    epsilon_heads = [
        production.head.value for production in wcnf.productions if not production.body
    ]
    terminal_productions = {
        production for production in wcnf.productions if len(production.body) == 1
    }
    variable_productions = {
        production for production in wcnf.productions if len(production.body) == 2
    }
    nodes_num = graph.number_of_nodes()

    boolean_matrices = {
        variable.value: sparse.dok_matrix((nodes_num, nodes_num), dtype=bool)
        for variable in wcnf.variables
    }

    for u, v, data in graph.edges(data=True):
        edge_label = data["label"]
        for variable in {
            terminal_production.head.value
            for terminal_production in terminal_productions
            if terminal_production.body[0].value == edge_label
        }:
            boolean_matrices[variable][u, v] = True

    for node_num in range(nodes_num):
        for variable in epsilon_heads:
            boolean_matrices[variable][node_num, node_num] = True

    changing = True
    while changing:
        changing = False

        for variable_production in variable_productions:
            current_nnz = boolean_matrices[variable_production.head.value].nnz
            boolean_matrices[variable_production.head.value] += (
                boolean_matrices[variable_production.body[0].value]
                @ boolean_matrices[variable_production.body[1].value]
            )
            next_nnz = boolean_matrices[variable_production.head.value].nnz
            changing = current_nnz != next_nnz

    reachable_node_nums = {
        (node_num_l, node_num_r)
        for node_num_l, node_num_r in zip(
            *boolean_matrices[wcnf.start_symbol.value].nonzero()
        )
    }

    if start_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_l in start_node_nums
        }

    if final_node_nums:
        reachable_node_nums = {
            (node_num_l, node_num_r)
            for node_num_l, node_num_r in reachable_node_nums
            if node_num_r in final_node_nums
        }

    return reachable_node_nums
