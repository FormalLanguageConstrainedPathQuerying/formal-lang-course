from pyformlang.finite_automaton import Symbol
from project import task2
from pyformlang.cfg import CFG, Variable, Terminal, Epsilon
from typing import Tuple
from scipy.sparse import dok_matrix, csr_matrix
import pyformlang
from pyformlang import *
import scipy
from pyformlang.regular_expression import Regex
from networkx import DiGraph
from pyformlang.finite_automaton.finite_automaton import to_symbol
import networkx as nx
from project import task3
from project.task2 import graph_to_nfa, regex_to_dfa
from pyformlang.rsa.box import Box
from pyformlang.rsa import RecursiveAutomaton


def cfg_to_rsm(cfg: pyformlang.cfg.CFG) -> pyformlang.rsa.RecursiveAutomaton:
    prods = {}
    for prod in cfg.productions:
        if len(prod.body) == 0:
            regex = []
            for var in prod.body:
                if isinstance(var, Epsilon):
                    regex.append("$")
                else:
                    regex.append(var.value)
            regex = " ".join(regex)
            regex = Regex(regex)
        else:
            regex = Regex("$")
        if Symbol(prod.head) not in prods:
            prods[Symbol(prod.head)] = regex
        else:
            prods[Symbol(prod.head)] = prods[Symbol(prod.head)].union(regex)

    for var, regex in prods.items():
        prods[Symbol(var)] = Box(regex.to_epsilon_nfa().to_deterministic(), Symbol(var))

    ans = pyformlang.rsa.RecursiveAutomaton(
        set(prods.keys()), Symbol("S"), set(prods.values())
    )

    return ans


def ebnf_to_rsm(ebnf: str) -> pyformlang.rsa.RecursiveAutomaton:
    prods = {}
    for p in ebnf.splitlines():
        p = p.strip()
        if "->" not in p:
            continue

        head, body = p.split("->")
        head = head.strip()
        if body.strip() != "":
            body = body.strip()
        else:
            body = Epsilon().to_text()

        if head in prods:
            prods[head] += " | " + body
        else:
            prods[head] = body

    for var, regex in prods.items():
        prods[Symbol(var)] = Box(
            Regex(regex).to_epsilon_nfa().to_deterministic(), Symbol(var)
        )

    return RecursiveAutomaton(set(prods.keys()), Symbol("S"), set(prods.values()))


def cfpq_with_tensor(
    rsm: pyformlang.rsa.RecursiveAutomaton,
    graph: DiGraph,
    start_nodes: set[int] = None,
    final_nodes: set[int] = None,
) -> set[tuple[int, int]]:

    if isinstance(rsm, CFG):
        rsm = cfg_to_rsm(rsm)

    graph_matrix = task3.nfa_to_mat(graph_to_nfa(graph, start_nodes, final_nodes))
    mat = task3.rsm_to_mat(rsm)
    graph_matrix_inds = graph_matrix.indexes_dict()
    mat_idx = mat.indexes_dict()

    n = graph_matrix.number_of_states

    for var in mat.null_symb:
        if var not in graph_matrix.basa:
            graph_matrix.basa[var] = dok_matrix((n, n), dtype=bool)
        graph_matrix.basa[var] += scipy.sparse.eye(n, dtype=bool)

    last = 0
    cur = None
    while cur != last:
        last = cur
        closure = task3.transitive_closure(
            task3.intersect_automata(mat, graph_matrix)
        ).nonzero()
        closure = list(zip(*closure))
        cur = len(closure)

        for i, j in closure:
            s = mat_idx[i // n]
            d = mat_idx[j // n]

            if s in mat.start_states and d in mat.final_states:
                var = s.value[0]
                if var not in graph_matrix.basa:
                    graph_matrix.basa[var] = dok_matrix((n, n), dtype=bool)
                graph_matrix.basa[var][i % n, j % n] = True

    result = set()
    for _, matrix in graph_matrix.basa.items():
        non_zero_indices = matrix.nonzero()
        for i, j in zip(*non_zero_indices):
            if (
                graph_matrix_inds[i] in mat.start_states
                and graph_matrix_inds[j] in mat.final_states
            ):
                result.add((graph_matrix_inds[i], graph_matrix_inds[j]))

    return result
