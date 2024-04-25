import pyformlang
import scipy
from project import task2
from pyformlang.cfg import CFG, Variable, Terminal, Epsilon
from typing import Tuple
from scipy.sparse import dok_matrix, csr_matrix
from networkx import DiGraph
from pyformlang.regular_expression import Regex
from project.task2 import graph_to_nfa, regex_to_dfa
from pyformlang.rsa.box import Box
from pyformlang.rsa import RecursiveAutomaton
from pyformlang.finite_automaton import Symbol
from pyformlang.finite_automaton.finite_automaton import to_symbol
import networkx as nx
from project import task3


def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    prods = {}
    for p in cfg.productions:
        if len(p.body) == 0:
            regex = Regex(
                " ".join(
                    "$" if isinstance(var, Epsilon) else var.value for var in p.body
                )
            )
        else:
            regex = Regex("$")
        if Symbol(p.head) not in prods:
            prods[Symbol(p.head)] = regex
        else:
            prods[Symbol(p.head)] = prods[Symbol(p.head)].union(regex)

    prods = {
        Symbol(var): Box(regex.to_epsilon_nfa().to_deterministic(), Symbol(var))
        for var, regex in prods.items()
    }

    return pyformlang.rsa.RecursiveAutomaton(
        set(prods.keys()), Symbol("S"), set(prods.values())
    )


def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    prods = {}
    boxes = set()
    for p in ebnf.splitlines():
        p = p.strip()
        if "->" not in p:
            continue

        head, body = p.split("->")
        head = head.strip()
        body = body.strip() if body.strip() != "" else Epsilon().to_text()

        if head in prods:
            prods[head] += " | " + body
        else:
            prods[head] = body

    prods = {
        Symbol(var): Box(Regex(regex).to_epsilon_nfa().to_deterministic(), Symbol(var))
        for var, regex in prods.items()
    }

    return RecursiveAutomaton(set(prods.keys()), Symbol("S"), set(prods.values()))


def cfpq_with_tensor(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:

    mat = task3.rsm_to_mat(rsm)
    graph_mat = task3.nfa_to_mat(graph_to_nfa(graph, start_nodes, final_nodes))
    mat_inds = mat.indexes_dict()
    graph_mat_inds = graph_mat.indexes_dict()

    n = graph_mat.states_count

    for var in mat.nullable_symbols:
        if var not in graph_mat.basa:
            graph_mat.basa[var] = dok_matrix((n, n), dtype=bool)
        graph_mat.basa[var] += scipy.sparse.eye(n, dtype=bool)

    last_nnz = 0
    while True:

        closure = task3.transitive_closure(
            task3.intersect_automata(mat, graph_mat)
        ).nonzero()
        closure = list(zip(*closure))

        curr_nnz = len(closure)
        if curr_nnz == last_nnz:
            break
        last_nnz = curr_nnz

        for i, j in closure:
            src = mat_inds[i // n]
            dst = mat_inds[j // n]

            if src in mat.start_states and dst in mat.final_states:
                var = src.value[0]
                if var not in graph_mat.basa:
                    graph_mat.basa[var] = dok_matrix((n, n), dtype=bool)
                graph_mat.basa[var][i % n, j % n] = True

    return {
        (graph_mat_inds[i], graph_mat_inds[j])
        for _, m in graph_mat.basa.items()
        for i, j in zip(*m.nonzero())
        if graph_mat_inds[i] in mat.start_states
        and graph_mat_inds[j] in mat.final_states
    }
