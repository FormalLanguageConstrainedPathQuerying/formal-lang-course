# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import random
from copy import deepcopy

import cfpq_data
import pytest
from networkx import MultiDiGraph

# Fix import statements in try block to run tests
try:
    from project.task4 import reachability_with_constraints
    from project.task2 import regex_to_dfa, graph_to_nfa
    from project.task3 import paths_ends, FiniteAutomaton
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
    n_of_nodes = random.randint(20, 40)
    return cfpq_data.graphs.generators.labeled_scale_free_graph(
        n_of_nodes, labels=LABEL
    )


@pytest.fixture(scope="class", params=range(5))
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
        fa = FiniteAutomaton(
            graph_to_nfa(deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes))
        )
        constraint_fa = FiniteAutomaton(regex_to_dfa(query))
        reachable: dict = reachability_with_constraints(
            deepcopy(fa), deepcopy(constraint_fa)
        )
        reachable = {k: v for k, v in reachable.items() if len(v) != 0}
        ends = paths_ends(
            deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes), query
        )

        assert len(set(reachable.keys())) == len(set(map(lambda x: x[0], ends)))

        equivalency_flag = True
        for start, final in ends:
            if start in reachable.keys() and final in reachable[start]:
                continue
            else:
                equivalency_flag = False
                break
        assert equivalency_flag
