# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import itertools
from pyformlang import cfg
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
import pytest
import random
import networkx as nx
from copy import deepcopy

# Fix import statements in try block to run tests
try:
    from project.task2 import graph_to_nfa, regex_to_dfa
    from project.task4 import reachability_with_constraints
    from project.task6 import cfg_to_weak_normal_form, cfpq_with_hellings
except ImportError:
    pytestmark = pytest.mark.skip("Task 6 is not ready to test!")

REGEXP_CFG: dict[str, list[cfg.CFG]] = {
    "a": [cfg.CFG.from_text("S -> a"), cfg.CFG.from_text("S -> N B\nB -> $\nN -> a")],
    "a*": [
        cfg.CFG.from_text("S -> $ | a S"),
        cfg.CFG.from_text("S -> $ | S S | a"),
        cfg.CFG.from_text("S -> S a S | $"),
    ],
    "abc": [cfg.CFG.from_text("S -> a b c"), cfg.CFG.from_text("S -> a B\nB -> b c")],
    "a*b*": [
        cfg.CFG.from_text("S -> S1 S2\nS2 -> $ | b S2\nS1 -> $ | a S1"),
        cfg.CFG.from_text("S -> $ | S1 | a S\nS1 -> $ | b S1"),
    ],
    "(ab)*": [
        cfg.CFG.from_text("S -> $ | a b S"),
        cfg.CFG.from_text("S -> $ | S S1\nS1 -> a b"),
    ],
    "ab*c*": [
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
        cfg.CFG.from_text("S -> $ | a S b | c S d | S S"),
        cfg.CFG.from_text("S -> $ | a S b S"),
        cfg.CFG.from_text("S -> $ | S a S b"),
        cfg.CFG.from_text("S -> $ | a S b | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | a S b | c S d | S S"),
        cfg.CFG.from_text("S -> $ | a S b S | c S d S"),
        cfg.CFG.from_text("S -> $ | S a S b | c S d S"),
        cfg.CFG.from_text("S -> $ | a S b | c S d S | S S S"),
    ],
    [
        cfg.CFG.from_text("S -> $ | S1 S S2\nS1 -> a | c\n S2 -> b | d"),
        cfg.CFG.from_text("S -> $ | S1 S S2 S\n S1 -> a | c\nS2 -> b | d"),
        cfg.CFG.from_text("S -> $ | S a S b | S a S d | S c S d | S c S b"),
        cfg.CFG.from_text("S -> $ | S1 S S2 | S S S\nS1 -> a | c\nS2-> b | d"),
    ],
    [
        cfg.CFG.from_text("S -> S S Se S1 Se\nSe -> $ | Se e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S1 | S S | e\nS1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> S2 S | $\n S2 -> e | S1\n S1 -> $ | a S1 b"),
        cfg.CFG.from_text("S -> $ |  S1 S | e S\n S1 -> $ | a S1 b"),
    ],
]

LABELS = ["a", "b", "c", "d", "e", "f", "g", "h"]

LABEL = "label"
IS_FINAL = "is_final"
IS_START = "is_start"


@pytest.fixture(scope="function", params=range(5))
def graph_s(request) -> MultiDiGraph:
    n_of_nodes = random.randint(1, 20)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data[LABEL] = random.choice(LABELS)
    return graph


@pytest.fixture(scope="function", params=range(5))
def graph_b(request) -> MultiDiGraph:
    n_of_nodes = random.randint(1, 40)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data[LABEL] = random.choice(LABELS)
    return graph


class TestReachability:
    @pytest.mark.parametrize(
        "regex_str, cfg_list", REGEXP_CFG.items(), ids=lambda regexp_cfgs: regexp_cfgs
    )
    def test_rpq_cfpq(self, graph_s, regex_str, cfg_list) -> None:
        regex = Regex(regex_str)
        start_nodes = set(
            random.choices(
                list(graph_s.nodes().keys()), k=random.randint(1, len(graph_s.nodes))
            )
        )
        final_nodes = set(
            random.choices(
                list(graph_s.nodes().keys()), k=random.randint(1, len(graph_s.nodes))
            )
        )
        for node, data in graph_s.nodes(data=True):
            if node in start_nodes:
                data[IS_START] = True
            if node in final_nodes:
                data[IS_FINAL] = True

        for cf_gram in cfg_list:
            cfpq: set[tuple[int, int]] = cfpq_with_hellings(
                cf_gram, deepcopy(graph_s), start_nodes, final_nodes
            )
            rpq: dict[int, set[int]] = reachability_with_constraints(
                regex_to_dfa(regex), graph_to_nfa(graph_s, start_nodes, final_nodes)
            )
            rpq_set = set()
            for node_from, nodes_to in rpq.items():
                for node_to in nodes_to:
                    rpq_set.add((node_from, node_to))
            if cfpq != rpq_set:
                assert False
        assert True

    @pytest.mark.parametrize("eq_grammars", GRAMMARS, ids=lambda grammars: grammars)
    def test_different_grammars(self, graph_b, eq_grammars):
        start_nodes = set(
            random.choices(
                list(graph_b.nodes().keys()), k=random.randint(1, len(graph_b.nodes))
            )
        )
        final_nodes = set(
            random.choices(
                list(graph_b.nodes().keys()), k=random.randint(1, len(graph_b.nodes))
            )
        )
        start_nodes = graph_b.nodes
        final_nodes = graph_b.nodes
        for node, data in graph_b.nodes(data=True):
            if node in start_nodes:
                data[IS_START] = True
            if node in final_nodes:
                data[IS_FINAL] = True
        eq_cfpqs = [
            cfpq_with_hellings(cf_gram, deepcopy(graph_b), start_nodes, final_nodes)
            for cf_gram in eq_grammars
        ]
        for a, b in itertools.combinations(eq_cfpqs, 2):
            if a != b:
                assert False
        assert True
