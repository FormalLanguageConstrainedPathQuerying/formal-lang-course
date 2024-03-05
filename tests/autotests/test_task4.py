# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import pyformlang.finite_automaton
from networkx import MultiDiGraph
from pyformlang.regular_expression import Regex
import pytest
import random
import itertools
import networkx as nx

# Fix import statements in try block to run tests
try:
    from project.task4 import reachability_with_constraints
    from project.task2 import regex_to_dfa, graph_to_nfa
    from project.task3 import paths_ends
except ImportError:
    pytestmark = pytest.mark.skip("Task 4 is not ready to test!")

QUERIES = [
    "a",
    "a*",
    "ab",
    "abc",
    "abcd",
    "a*b*",
    "(ab)*",
    "ab*",
    "ab*c*",
    "ab*c",
    "abc*",
    "(a|b|c|d|e)*",
    "(a|b|c|d|e)(a|b|c|d|e)*",
    "(a|b|c|d|e)f*",
    "(a|b)*",
    "(a|b)*(c|d)*",
    "(a | b)*(c | d)*(e | f)*",
    "(a | b | c)*(d | e | f)*",
    "((a|b)*c)*",
    "((a | b) * c)*(d | e)",
    "((a | b)*c)*((d | e)*f)*",
]
LABELS = ["a", "b", "c", "d", "e", "f", "g", "h"]

LABEL = "label"
IS_FINAL = "is_final"
IS_START = "is_start"


@pytest.fixture(scope="class", params=range(5))
def graph(request) -> MultiDiGraph:
    n_of_nodes = random.randint(1, 20)
    graph = nx.scale_free_graph(n_of_nodes)

    for _, _, data in graph.edges(data=True):
        data[LABEL] = random.choice(LABELS)
    return graph


@pytest.fixture(scope="class", params=range(10))
def query(request) -> str:
    return random.choice(QUERIES)


class TestReachability:
    def test(self, graph, query) -> None:
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
        fa = graph_to_nfa(graph, start_nodes, final_nodes)
        constraint_fa = regex_to_dfa(Regex(query))
        reachable: dict = reachability_with_constraints(fa, constraint_fa)
        ends = paths_ends(graph, start_nodes, final_nodes, query)

        equivalency_flag = True
        for start, final in ends:
            if start in reachable.keys() and final in reachable[start]:
                continue
            else:
                equivalency_flag = False
                break
        assert equivalency_flag
