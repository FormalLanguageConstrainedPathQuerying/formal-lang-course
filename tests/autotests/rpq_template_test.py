from copy import deepcopy
from helper import generate_rnd_start_and_final
from networkx import MultiDiGraph
from pyformlang.cfg import CFG
from pyformlang.rsa import RecursiveAutomaton
from typing import Callable, Iterable

try:
    from project.bfs_rpq import ms_bfs_based_rpq
except ImportError:
    pass


def rpq_cfpq_test(
    graph: MultiDiGraph,
    regex_str: str,
    cfg_list: Iterable[CFG | RecursiveAutomaton],
    function: Callable[
        [CFG | RecursiveAutomaton, MultiDiGraph, set[int], set[int]],
        set[tuple[int, int]],
    ],
) -> None:
    start_nodes, final_nodes = generate_rnd_start_and_final(graph)
    for cf_gram in cfg_list:
        cfpq: set[tuple[int, int]] = function(
            cf_gram, deepcopy(graph), start_nodes, final_nodes
        )
        rpq: set[tuple[int, int]] = ms_bfs_based_rpq(
            regex_str, deepcopy(graph), start_nodes, final_nodes
        )

        assert cfpq == rpq


def different_grammars_test(
    graph: MultiDiGraph,
    eq_grammars: Iterable[CFG | RecursiveAutomaton],
    function: Callable[
        [CFG | RecursiveAutomaton, MultiDiGraph, set[int], set[int]],
        set[tuple[int, int]],
    ],
) -> None:
    start_nodes, final_nodes = generate_rnd_start_and_final(graph)
    eq_cfpqs = [
        function(cf_gram, deepcopy(graph), start_nodes, final_nodes)
        for cf_gram in eq_grammars
    ]
    assert eq_cfpqs.count(eq_cfpqs[0]) == len(eq_cfpqs)


def cfpq_algorithm_test(
    graph: MultiDiGraph,
    ebnf_list: Iterable[str],
    cfg_list: Iterable[CFG],
    ebnf_to_rsm: Callable[[str], RecursiveAutomaton],
    cfg_to_rsm: Callable[[CFG], RecursiveAutomaton],
    function: Callable[
        [RecursiveAutomaton, MultiDiGraph, set[int], set[int]], set[tuple[int, int]]
    ],
) -> None:
    start_nodes, final_nodes = generate_rnd_start_and_final(graph)
    rsm_list = []
    rsm_list.extend(ebnf_to_rsm(ebnf) for ebnf in ebnf_list)
    rsm_list.extend(cfg_to_rsm(cfg) for cfg in cfg_list)
    eq_cfpqs = [
        function((deepcopy(rsm)), deepcopy(graph), start_nodes, final_nodes)
        for rsm in rsm_list
    ]
    assert eq_cfpqs.count(eq_cfpqs[0]) == len(eq_cfpqs)
