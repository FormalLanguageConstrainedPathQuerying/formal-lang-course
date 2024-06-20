import networkx as nx
import pyformlang
from typing import Set
from pyformlang.cfg import Terminal
from scipy.sparse import lil_matrix
from project.task6.grammar_transform import cfg_to_weak_normal_form


def cfpq_with_matrix(
    grammar: pyformlang.cfg.CFG,
    graph_data: nx.DiGraph,
    start_set: Set[int] = None,
    final_set: Set[int] = None,
) -> Set[tuple[int, int]]:
    """
    Computes the context-free path querying (CFPQ) using matrix-based algorithm.

    Parameters:
    -----------
    grammar : pyformlang.cfg.CFG
        The context-free grammar for path querying.
    graph_data : nx.DiGraph
        The directed graph to query.
    start_set : Set[int], optional
        The set of start nodes. If None, all nodes are considered start nodes.
    final_set : Set[int], optional
        The set of final nodes. If None, all nodes are considered final nodes.

    Returns:
    --------
    Set[Tuple[int, int]]
        A set of node pairs (i, j) such that there is a path from i to j
        in the graph that matches the given grammar.
    """
    grammar = cfg_to_weak_normal_form(grammar)

    nonterminals_set = {rule.head for rule in grammar.productions}
    var_indices = {var: idx for idx, var in enumerate(nonterminals_set)}

    # Создаем разреженные матрицы смежности для каждого нетерминала
    adj_matrices_dict = {
        variable: lil_matrix(
            (graph_data.number_of_nodes(), graph_data.number_of_nodes()), dtype=bool
        )
        for variable in nonterminals_set
    }

    # Инициализируем матрицы смежности для правил с терминалами
    for rule in grammar.productions:
        if len(rule.body) == 1 and isinstance(rule.body[0], Terminal):
            terminal = rule.body[0]
            for u, v, data in graph_data.edges(data=True):
                if str(data.get("label", "")) == str(terminal):
                    adj_matrices_dict[rule.head][u, v] = True

    # обновляем матрицы до тех пор, пока они изменяются
    while True:
        is_changed = False
        for rule in grammar.productions:
            if len(rule.body) == 2:
                matrix_a, matrix_b = rule.body
                if matrix_a in var_indices and matrix_b in var_indices:
                    before_change = adj_matrices_dict[rule.head].nnz
                    adj_matrices_dict[rule.head] += (
                        adj_matrices_dict[matrix_a] * adj_matrices_dict[matrix_b]
                    )
                    after_change = adj_matrices_dict[rule.head].nnz
                    if before_change != after_change:
                        is_changed = True
        if not is_changed:
            break

    # Строим результирующее множество
    result_set = set()
    start_symbol = grammar.start_symbol
    if start_symbol in adj_matrices_dict:
        matrix_data = adj_matrices_dict[start_symbol].tocoo()
        for i, j in zip(matrix_data.row, matrix_data.col):
            if (start_set is None or i in start_set) and (
                final_set is None or j in final_set
            ):
                result_set.add((i, j))

    return result_set
