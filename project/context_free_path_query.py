import collections
from enum import Enum
from functools import reduce

import numpy as np
from networkx import MultiDiGraph
from pyformlang.cfg import CFG, Terminal, Variable
from pyformlang.finite_automaton import Symbol, State
from scipy.sparse import dok_matrix

from project.automata_utils import get_enfa_edges
from project.boolean_decomposition import BooleanDecomposition, boolean_decompose_enfa
from project.cfg_utils import from_cfg_to_weak_cnf

__all__ = ["context_free_path_query", "Algorithm"]

from project.ecfg import ECFG
from project.graph_utils import from_graph_to_nfa

from project.recursive_automata import RecursiveAutomata


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


def tensor_transitive_closure(
    graph: MultiDiGraph, cfg: CFG
) -> set[tuple[any, Variable, any]]:
    automata = RecursiveAutomata.from_ecfg(ECFG.from_pyformlang_cfg(cfg))
    variables = cfg.variables
    terminals = cfg.terminals
    start_states = reduce(
        lambda acc, l: acc + l,
        [
            list(zip(a.start_states, [var for _ in range(len(a.start_states))]))
            for var, a in automata.variable_to_automata.items()
        ],
    )
    final_states = reduce(
        lambda acc, l: acc + l,
        [
            list(zip(a.final_states, [var for _ in range(len(a.final_states))]))
            for var, a in automata.variable_to_automata.items()
        ],
    )
    all_states = reduce(
        lambda acc, l: acc + l,
        [
            list(zip(a.states, [var for _ in range(len(a.states))]))
            for var, a in automata.variable_to_automata.items()
        ],
    )

    # boolean decompose graph and cfg`s recursive automata
    automata_size = len(all_states)
    symbol_to_matrix = dict()
    for var in variables:
        mat = dok_matrix((automata_size, automata_size), dtype=np.int32)
        for enfa_var, enfa in automata.variable_to_automata.items():
            for (v, symbol, u) in get_enfa_edges(enfa):
                if var.value == symbol.value:
                    mat[
                        all_states.index((v, enfa_var)), all_states.index((u, enfa_var))
                    ] = 1
        symbol_to_matrix[Symbol(var.value)] = mat
    for term in terminals:
        mat = dok_matrix((automata_size, automata_size), dtype=np.int32)
        for enfa_var, enfa in automata.variable_to_automata.items():
            for (v, symbol, u) in get_enfa_edges(enfa):
                if term.value == symbol.value:
                    mat[
                        all_states.index((v, enfa_var)), all_states.index((u, enfa_var))
                    ] = 1
        symbol_to_matrix[Symbol(term.value)] = mat

    boolean_decomposition_automata = BooleanDecomposition(
        symbol_to_matrix, list(map(lambda s: State(s), all_states))
    )
    boolean_decomposition_graph = boolean_decompose_enfa(from_graph_to_nfa(graph))

    # add new edges in initial graph with epsilon variables
    result = set()

    graph_size = len(graph.nodes)
    graph_nodes = list(graph.nodes)
    for production in cfg.productions:
        if len(production.body) == 0:
            symbol = Symbol(production.head.value)
            symbols_to_matrix = boolean_decomposition_graph.symbols_to_matrix
            if symbol not in symbols_to_matrix:
                symbols_to_matrix[symbol] = dok_matrix(
                    (graph_size, graph_size), dtype=np.int32
                )
            for i in range(graph_size):
                symbols_to_matrix[symbol][i, i] = 1
                result.add((graph_nodes[i], production.head, graph_nodes[i]))

    # algorithm
    while True:
        result_size = len(result)
        kron_decomposition = boolean_decomposition_automata.kron(
            boolean_decomposition_graph
        )
        transitive_closure = kron_decomposition.transitive_closure()
        for (i, j) in zip(*transitive_closure.nonzero()):
            (s, x) = kron_decomposition.states()[i].value
            (f, y) = kron_decomposition.states()[j].value
            if s.value in start_states and f.value in final_states:
                symbol = Symbol(s.value[1])
                if symbol not in boolean_decomposition_graph.symbols_to_matrix:
                    boolean_decomposition_graph.symbols_to_matrix[symbol] = dok_matrix(
                        (graph_size, graph_size), dtype=np.int32
                    )
                boolean_decomposition_graph.symbols_to_matrix[symbol][
                    boolean_decomposition_graph.state_index(x.value),
                    boolean_decomposition_graph.state_index(y.value),
                ] = 1
                result.add((x.value, s.value[1], y.value))

        if len(result) == result_size:
            break

    return result


class Algorithm(Enum):
    """
    Algorithms that can be used to context free path query
    """

    HELLINGS = hellings_transitive_closure
    MATRIX = matrix_transitive_closure
    TENSOR = tensor_transitive_closure


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
