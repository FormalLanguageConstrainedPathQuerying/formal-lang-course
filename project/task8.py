from project.task2 import graph_to_nfa

from pyformlang.finite_automaton import TransitionFunction, EpsilonNFA, Symbol, State
from pyformlang.rsa import RecursiveAutomaton, Box
from pyformlang.cfg import CFG

import networkx as nx
from itertools import *
from scipy.sparse import *

from project.task3 import FiniteAutomaton, rsm_to_fa


def cfpq_with_tensor(
    rsm: RecursiveAutomaton,
    graph: nx.MultiDiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:
    if isinstance(rsm, CFG):
        rsm = cfg_to_rsm(rsm)

    if start_nodes is None:
        start_nodes = graph.nodes
    if final_nodes is None:
        final_nodes = graph.nodes

    rsm_fa = rsm_to_fa(rsm)
    rsm_n_states = len(rsm_fa.states)
    graph_fa = FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes))
    mapping = {
        i: state for i, state in enumerate(product(graph_fa.states, rsm_fa.states))
    }

    graph_n_states = len(graph_fa.states)

    zeros = 0
    while True:
        n = rsm_n_states * graph_n_states
        symbols = rsm_fa.matrix.keys() & graph_fa.matrix.keys()
        if len(symbols) != 0:
            mat = {}
            for symbol in symbols:
                mat[symbol] = kron(graph_fa.matrix[symbol], rsm_fa.matrix[symbol])
            m = sum(mat.values())
        else:
            m = dok_matrix((n, n), dtype=bool)
        m += eye(n, dtype=bool)

        for _ in range(n):
            m += m @ m

        new_zeros = m.count_nonzero()
        if new_zeros <= zeros:
            break
        else:
            zeros = new_zeros

        for fr, to in zip(*m.nonzero()):
            from_state = mapping[fr]
            to_state = mapping[to]
            from_rsm_state = from_state[1]
            to_rsm_state = to_state[1]
            if (
                from_rsm_state in rsm_fa.start_states
                and to_rsm_state in rsm_fa.final_states
            ):
                N = from_rsm_state[0]
                graph_from = graph_fa.states_to_int[from_state[0]]
                graph_to = graph_fa.states_to_int[to_state[0]]
                graph_fa.matrix.setdefault(
                    N, dok_matrix((graph_n_states, graph_n_states), dtype=bool)
                )[graph_from, graph_to] = True

    S = rsm.initial_label.value
    if S not in graph_fa.matrix:
        return set()

    res = set()
    for graph_from_state, graph_to_state in product(start_nodes, final_nodes):
        graph_from = graph_fa.states_to_int[graph_from_state]
        graph_to = graph_fa.states_to_int[graph_to_state]
        if graph_fa.matrix[S][graph_from, graph_to]:
            res.add((graph_from_state, graph_to_state))
    return res


def cfg_to_rsm(cfg: CFG) -> RecursiveAutomaton:
    return RecursiveAutomaton.from_text(cfg.to_text())


def ebnf_to_rsm(ebnf: str) -> RecursiveAutomaton:
    return RecursiveAutomaton.from_text(ebnf)
