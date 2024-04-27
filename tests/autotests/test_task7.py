# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import itertools
import random
from copy import deepcopy
import cfpq_data as cd
import networkx as nx
import pytest
from networkx import MultiDiGraph
from pyformlang import cfg

# Fix import statements in try block to run tests
try:
    from project.task7 import cfpq_with_matrix
    from project.task2 import graph_to_nfa, regex_to_dfa
    from project.task3 import FiniteAutomaton
    from project.task4 import reachability_with_constraints
    from project.task6 import cfpq_with_hellings
except ImportError:
    pytestmark = pytest.mark.skip("Task 7 is not ready to test!")

REGEXP_CFG: dict[str, list[cfg.CFG]] = {
    "a": [cfg.CFG.from_text("S -> a"), cfg.CFG.from_text("S -> N B\nB -> $\nN -> a")],
    "a*": [
        cfg.CFG.from_text("S -> $ | a S"),
        cfg.CFG.from_text("S -> $ | S S | a"),
        cfg.CFG.from_text("S -> S a S | $"),
    ],
    "a b c": [cfg.CFG.from_text("S -> a b c"), cfg.CFG.from_text("S -> a B\nB -> b c")],
    "a*b*": [
        cfg.CFG.from_text("S -> S1 S2\nS2 -> $ | b S2\nS1 -> $ | a S1"),
        cfg.CFG.from_text("S -> $ | S1 | a S\nS1 -> $ | b S1"),
    ],
    "(a b)*": [
        cfg.CFG.from_text("S -> $ | a b S"),
        cfg.CFG.from_text("S -> $ | S S1\nS1 -> a b"),
    ],
    "a b*c*": [
        cfg.CFG.from_text("S -> S1 S2 S3\nS1 -> a\nS2 -> $ | S2 b\nS3 -> $ | c S3"),
        cfg.CFG.from_text("S -> a S2 S3\nS2 -> S2 b | $\nS3 -> c | $ | S3 S3"),
    ],
    "(a|b|c|d|e)*": [
        cfg.CFG.from_text("S -> $ | S1 S\nS1 -> a | b | c | d | e"),
        cfg.CFG.from_text("S -> $ | a | b | c | d | e | S S"),
        cfg.CFG.from_text("S -> $ | a S | b S | c S | e S | d S"),
    ],
    "((a | b) * c)*(d | e)": [
        cfg.CFG.from_text(
            "S -> S1 S2\nS1 -> S1 S1 | $ | S3 c\n S2 -> d | e\n S3 -> b S3 | $ | a S3"
        ),
        cfg.CFG.from_text("S -> S1 d | S1 e\nS1 -> S1 S3 c | $\nS3 -> b S3 | $ | a S3"),
    ],
}

GRAMMARS = [
    [
        cfg.CFG.from_text("S -> $ | a S b | S S"),
        cfg.CFG.from_text("S -> $ | a S b S"),
        cfg.CFG.from_text("S -> $ | S a S b"),
        cfg.CFG.from_text("S -> $ | a S b | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | a S b | c S d | S S"),
        cfg.CFG.from_text("S -> $ | a S b S | c S d S"),
        cfg.CFG.from_text("S -> $ | S a S b | S c S d"),
        cfg.CFG.from_text("S -> $ | a S b | c S d S | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | S1 S S2\nS1 -> a | c\n S2 -> b | d\n S -> S S"),
        cfg.CFG.from_text("S -> $ | S1 S S2 S\n S1 -> a | c\nS2 -> b | d"),
        cfg.CFG.from_text("S -> $ | S a S b | S a S d | S c S d | S c S b"),
        cfg.CFG.from_text("S -> $ | S1 S S2 | S S S\nS1 -> a | c\nS2-> b | d"),
    ],
    [
        cfg.CFG.from_text("S -> S S | Se S1 Se\nSe -> $ | Se e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S1 | S S | e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S2 S | $\n S2 -> e | S1\n S1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> $ | S1 S | e S\n S1 -> $ | a S1 b"),
    ],
    [
        cfg.CFG.from_text("S -> a S | $"),
        cfg.CFG.from_text("S -> S1 | a\nS1 -> a S1 | $"),
    ],
]

GRAMMARS_DIFFERENT = [
    cfg.CFG.from_text(
        "S -> S1 | S2\nS1 -> Sab | S1 c\nSab -> $ | a Sab b\nS2 -> Sbc | a S2\nSbc -> b Sbc c"
    ),
    cfg.CFG.from_text("S -> a | b | S c S | S d S | e S f | g S"),
    cfg.CFG.from_text("S -> $ | a S b | b S a | e S f | S S | c S d | f S c | f S e"),
]

LABELS = ["a", "b", "c", "d", "e", "f", "g", "h"]

LABEL = "label"
IS_FINAL = "is_final"
IS_START = "is_start"


def generate_rnd_start_and_final(graph):
    start_nodes = set(
        random.choices(
            list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
        )
    )
    final_nodes = set(
        random.choices(
            list(graph.nodes().keys()), k=random.randint(1, len(graph.nodes))
        )
    )

    for node, data in graph.nodes(data=True):
        if node in start_nodes:
            data[IS_START] = True
        if node in final_nodes:
            data[IS_FINAL] = True
    return start_nodes, final_nodes


@pytest.fixture(scope="function", params=range(5))
def graph(request) -> MultiDiGraph:
    n_of_nodes = random.randint(20, 40)
    return cd.graphs.labeled_scale_free_graph(n_of_nodes, labels=LABELS)


class TestReachabilityMatrixAlgorithm:
    @pytest.mark.parametrize(
        "regex_str, cfg_list", REGEXP_CFG.items(), ids=lambda regexp_cfgs: regexp_cfgs
    )
    def test_rpq_cfpq_matrix(self, graph, regex_str, cfg_list) -> None:
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)

        for cf_gram in cfg_list:
            cfpq: set[tuple[int, int]] = cfpq_with_matrix(
                cf_gram, deepcopy(graph), start_nodes, final_nodes
            )
            rpq: dict[int, set[int]] = reachability_with_constraints(
                FiniteAutomaton(graph_to_nfa(graph, start_nodes, final_nodes)),
                FiniteAutomaton(regex_to_dfa(regex_str)),
            )
            rpq_set = set()
            for node_from, nodes_to in rpq.items():
                for node_to in nodes_to:
                    rpq_set.add((node_from, node_to))
            assert cfpq == rpq_set

    @pytest.mark.parametrize("eq_grammars", GRAMMARS, ids=lambda grammars: grammars)
    def test_different_grammars(self, graph, eq_grammars):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        eq_cfpqs = [
            cfpq_with_matrix(
                deepcopy(cf_gram), deepcopy(graph), start_nodes, final_nodes
            )
            for cf_gram in eq_grammars
        ]
        for a, b in itertools.combinations(eq_cfpqs, 2):
            assert a == b

    @pytest.mark.parametrize("grammar", GRAMMARS_DIFFERENT, ids=lambda g: g)
    def test_hellings_matrix(self, graph, grammar):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        hellings = cfpq_with_hellings(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        matrix = cfpq_with_matrix(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        assert hellings == matrix
