import itertools
from copy import deepcopy
from helper import generate_rnd_start_and_final, rpq_dict_to_set

try:
    from project.task2 import graph_to_nfa, regex_to_dfa
    from project.task3 import FiniteAutomaton
    from project.task4 import reachability_with_constraints
except ImportError:
    pass


def rpq_cfpq_test(graph, regex_str, cfg_list, function) -> None:
    start_nodes, final_nodes = generate_rnd_start_and_final(graph)
    for cf_gram in cfg_list:
        cfpq: set[tuple[int, int]] = function(
            cf_gram, deepcopy(graph), start_nodes, final_nodes
        )
        rpq: set[tuple[int, int]] = rpq_dict_to_set(
            reachability_with_constraints(
                FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes)),
                FiniteAutomaton(regex_to_dfa(regex_str)),
            )
        )
        assert cfpq == rpq


def different_grammars_test(graph, eq_grammars, function):
    start_nodes, final_nodes = generate_rnd_start_and_final(graph)
    eq_cfpqs = [
        function(deepcopy(cf_gram), deepcopy(graph), start_nodes, final_nodes)
        for cf_gram in eq_grammars
    ]
    for a, b in itertools.combinations(eq_cfpqs, 2):
        assert a == b
