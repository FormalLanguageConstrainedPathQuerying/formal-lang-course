from pyformlang.finite_automaton import EpsilonNFA
from pyformlang.regular_expression import Regex
from project.requests import regex_to_dka, graph_to_nka
from networkx.classes.multidigraph import MultiDiGraph
import numpy as np
import scipy.sparse as sp
from typing import Tuple, Dict


def fa_to_matrix(fa: EpsilonNFA) -> Tuple[Dict, Dict]:
    """
        To a dictionary of matrices
        Arguments:
            fa: EpsilonDFA
        Returns:
            Two dictionaries: transition matrices for symbols and states ids for state labels
    """
    res = dict()
    ss = {s: i for i, s in enumerate(fa.states)}
    for s, l, f in fa:
        if l not in res:
            res[l] = sp.dok_matrix((len(fa.states), len(fa.states)), dtype=np.bool_)
        res[l][ss[s], ss[f]] = True
    return res, ss


def reachable_vertices(reg: EpsilonNFA, g: MultiDiGraph, ss: [int], fe: bool = False):
    """
    Finds graph reachable vertices
    Arguments:
        reg: regex EpsilonNFA
        g: graph for request
        ss: list of states from which reachability will be searched
        fe: boolean - for each start state or not
    Returns:
        Dict of reachable states
    """
    (ra, rm) = fa_to_matrix(reg)
    (ga, gm) = fa_to_matrix(graph_to_nka(g, [], []))
    rml = len(rm)

    sc = set(ra.keys()).intersection(set(ga.keys()))

    ts = {s: sp.block_diag((ra[s], ga[s])).transpose() for s in sc}

    if not fe:
        sets = {frozenset(ss)}
    else:
        sets = {frozenset({x}) for x in ss}

    res = {}
    for s1 in sets:
        c = {(rm[r], gm[ss1]) for r in reg.start_states for ss1 in s1}
        used = set()
        while c:
            used = used | c
            f = sp.dok_matrix((len(gm), rml), dtype=np.bool_)
            for (s, d) in c:
                f[d, s] = True
            f = sp.vstack((sp.identity(rml, dtype=np.bool_), f), format="csr")
            c = set()
            for l, m in ts.items():
                rs = [[]] * rml
                gs = [[]] * rml
                nf = sp.coo_matrix(m @ f)
                for s, d, v in zip(nf.row, nf.col, nf.data):
                    if v:
                        if s < rml:
                            rs[d].append(s)
                        else:
                            gs[d].append(s - rml)

                c = c | {(s, d) for i in range(rml) for s in rs[i] for d in gs[i]}
            c = c - used
        res[frozenset(s1)] = {j for i, j in used if i in {rm[i] for i in reg.final_states}}

    gs = [j for a, j in sorted([(id, l) for l, id in gm.items()])]

    if not fe:
        (bs,) = res.values()
        return {gs[id] for id in bs}
    else:
        return {s: {gs[d] for d in ds} for (s,), ds in res.items()}


def bfs_graph_request(g: MultiDiGraph, ss: [int], fs: [int], regex: str, fe: bool = False):
    """
    Regex request for graph using BFS
    Arguments:
        g: graph
        ss: list of start states
        fs: list of final states
        regex: regex for request
        fe: boolean - for each start state or not
    Returns:
        Dict of states
    """
    res = reachable_vertices(regex_to_dka(Regex(regex)), g, ss, fe)

    if not fe:
        return {s for s in res if s in fs}
    if fe:
        return {state: {d for d in ds if d in fs} for state, ds in res.items()}
