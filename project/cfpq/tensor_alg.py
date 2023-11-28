import networkx as nx
from scipy.sparse import dok_matrix
from pyformlang.cfg import CFG, Variable
from scipy.sparse import dok_matrix, identity

from project.automaton_utils import graph_to_nfa
from project.cfpq.bool_dec import BooleanDecomposition


def tensor_alg(
    graph: nx.MultiDiGraph, cfg: CFG
) -> set[tuple[int, str, int]]:  # (node, nonterminal, node)
    n = sum(len(production.body) + 1 for production in cfg.productions)
    rsm_heads = dict()
    nonterm = set()
    boxes = dict()
    start_states = set()
    final_states = set()
    counter = 0

    nfa_by_graph = graph_to_nfa(graph)
    decomposition = BooleanDecomposition.from_automaton(nfa_by_graph)

    for production in cfg.productions:
        nonterm.add(production.head.value)
        start_states.add(counter)
        final_states.add(counter + len(production.body))
        rsm_heads[(counter, counter + len(production.body))] = production.head.value
        for b in production.body:
            m = boxes.get(b.value, dok_matrix((n, n), dtype=bool))
            m[counter, counter + 1] = True
            boxes[b.value] = m
            counter += 1
        counter += 1

    for production in cfg.productions:
        if len(production.body) == 0:
            decomposition.bool_matrices[production.head.value] = identity(
                decomposition.num_states, dtype=bool
            ).todok()

    changed = True
    bfa = BooleanDecomposition()
    bfa.start_states = start_states
    bfa.final_states = final_states
    bfa.bool_matrices = boxes
    bfa.states_count = n

    while changed:
        changed = False
        transitive_closure = bfa.intersect(decomposition).transitive_closure()
        x, y = transitive_closure.nonzero()

        for (i, j) in zip(x, y):
            rfa_from = i // decomposition.num_states
            rfa_to = j // decomposition.num_states
            graph_from = i % decomposition.num_states
            graph_to = j % decomposition.num_states

            if (rfa_from, rfa_to) not in rsm_heads:
                continue

            variable = rsm_heads[(rfa_from, rfa_to)]
            m = decomposition.bool_matrices.get(
                variable,
                dok_matrix(
                    (decomposition.num_states, decomposition.num_states), dtype=bool
                ),
            )
            if not m[graph_from, graph_to]:
                changed = True
                m[graph_from, graph_to] = True
                decomposition.bool_matrices[variable] = m

    result = set()
    for key, m in decomposition.bool_matrices.items():
        if key not in nonterm:
            continue
        for (u, v) in m.keys():
            result.add((u, key, v))

    return result


def tensor_cfpq(
    graph: nx.MultiDiGraph,
    cfg: CFG,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
    start_var: Variable = Variable("S"),
) -> set[tuple[int, int]]:
    cfg._start_symbol = start_var
    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes
    return {
        (u, v)
        for u, var, v in tensor_alg(graph, cfg)
        if var == cfg.start_symbol and u in start_nodes and v in final_nodes
    }
