import collections
from enum import Enum

import numpy as np
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Terminal, Variable
from scipy.sparse import dok_matrix

from project.cfg_utils import from_cfg_to_weak_cnf

__all__ = ["context_free_path_query", "Algorithm"]


def hellings_transitive_closure(
    graph: MultiDiGraph, cfg: CFG
) -> set[tuple[any, Variable, any]]:
    cfg = from_cfg_to_weak_cnf(cfg)

    # helpers
    terminal_to_variable = dict()
    pair_variables_to_variable = dict()
    epsilon_variables = set()

    for production in cfg.productions:
        match production.body:
            case []:
                epsilon_variables.add(production.head)
            case [Terminal() as term]:
                if term not in terminal_to_variable:
                    terminal_to_variable[term.value] = set()
                terminal_to_variable[term.value].add(production.head)
            case [Variable() as var1, Variable() as var2]:
                if (var1, var2) not in pair_variables_to_variable:
                    pair_variables_to_variable[(var1, var2)] = set()
                pair_variables_to_variable[(var1, var2)].add(production.head)

    # initialize
    result = set()

    for v, u, ddict in graph.edges(data=True):
        label = ddict["label"]
        if label in terminal_to_variable:
            for var in terminal_to_variable[label]:
                result.add((v, var, u))

    for node in graph.nodes:
        for var in epsilon_variables:
            result.add((node, var, node))

    queue = collections.deque(result)

    # main cycle of hellings
    while len(queue) > 0:
        subresult = set()
        v, var1, u = queue.popleft()
        for triple in result:
            if triple[2] != v:
                continue
            var0 = triple[1]
            start = triple[0]
            if (var0, var1) not in pair_variables_to_variable:
                continue
            for var in pair_variables_to_variable[(var0, var1)]:
                if (start, var, u) in result:
                    continue
                queue.append((start, var, u))
                subresult.add((start, var, u))
        for triple in result:
            if triple[0] != u:
                continue
            var2 = triple[1]
            end = triple[2]
            if (var1, var2) not in pair_variables_to_variable:
                continue
            for var in pair_variables_to_variable[(var1, var2)]:
                if (v, var, end) in result:
                    continue
                queue.append((v, var, end))
                subresult.add((v, var, end))
        result = result.union(subresult)

    return result


def matrix_transitive_closure(
    graph: MultiDiGraph, cfg: CFG
) -> set[tuple[any, Variable, any]]:
    cfg = from_cfg_to_weak_cnf(cfg)

    # helpers
    terminal_to_variable = dict()
    pair_variables_to_variables = dict()
    epsilon_variables = set()

    for production in cfg.productions:
        match production.body:
            case []:
                epsilon_variables.add(production.head)
            case [Terminal() as term]:
                if term not in terminal_to_variable:
                    terminal_to_variable[term.value] = set()
                terminal_to_variable[term.value].add(production.head)
            case [Variable() as var1, Variable() as var2]:
                if (var1, var2) not in pair_variables_to_variables:
                    pair_variables_to_variables[(var1, var2)] = set()
                pair_variables_to_variables[(var1, var2)].add(production.head)

    # initialize
    boolean_decomposition_dok_result = dict()

    nodes = list(graph.nodes)
    graph_size = len(nodes)
    for var in cfg.variables:
        boolean_decomposition_dok_result[var] = dok_matrix(
            (graph_size, graph_size), dtype=np.int32
        )

    for vnode, unode, ddict in graph.edges(data=True):
        label = ddict["label"]
        v = nodes.index(vnode)
        u = nodes.index(unode)
        if label in terminal_to_variable:
            for var in terminal_to_variable[label]:
                boolean_decomposition_dok_result[var][v, u] = 1

    for vnode in graph.nodes:
        v = nodes.index(vnode)
        for var in epsilon_variables:
            boolean_decomposition_dok_result[var][v, v] = 1

    boolean_decomposition_result = dict()
    for k, v in boolean_decomposition_dok_result.items():
        boolean_decomposition_result[k] = v.tocsr()

    # main cycle of matrix algorithm
    make_iteration = True
    while make_iteration:
        last_nnz = sum([m.getnnz() for m in boolean_decomposition_result.values()])

        for (var1, var2), variables in pair_variables_to_variables.items():
            for var in variables:
                boolean_decomposition_result[var] += (
                    boolean_decomposition_result[var1]
                    @ boolean_decomposition_result[var2]
                )

        make_iteration = last_nnz != sum(
            [m.getnnz() for m in boolean_decomposition_result.values()]
        )

    # formatting result
    result = set()
    for var, mat in boolean_decomposition_result.items():
        rows, cols = mat.nonzero()
        for i in range(len(rows)):
            result.add((nodes[rows[i]], var, nodes[cols[i]]))

    return result


class Algorithm(Enum):
    """
    Algorithms that can be used to context free path query
    """

    HELLINGS = hellings_transitive_closure
    MATRIX = matrix_transitive_closure


def context_free_path_query(
    cfg: CFG,
    graph: MultiDiGraph,
    start_variable: Variable = Variable("S"),
    start_nodes: list[any] = None,
    final_nodes: list[any] = None,
    algorithm: Algorithm = Algorithm.MATRIX,
) -> set[tuple[any, any]]:
    """
    Performs cfpq (context free path query) in graph with given context free grammar
    :param algorithm: algorithm to make cfpq
    :param cfg: context free grammar to perform cfpq
    :param graph: graph to be inspected
    :param start_variable: start non terminal symbol to make query
    :param start_nodes: start nodes to cfpq inside graph (all nodes if None)
    :param final_nodes: final nodes to cfpq inside graph (all nodes if None)
    :return: 2 element tuples with nodes satisfying cfpq
    """
    if start_nodes is None:
        start_nodes = list(graph.nodes)

    if final_nodes is None:
        final_nodes = list(graph.nodes)

    result = algorithm(graph, cfg)
    return set(
        [
            (u, v)
            for u, var, v in result
            if var == start_variable and u in start_nodes and v in final_nodes
        ]
    )
