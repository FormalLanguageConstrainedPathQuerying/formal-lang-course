# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
import random
from copy import deepcopy
import pytest
from grammars_constants import REGEXES
from helper import generate_rnd_start_and_final, rpq_dict_to_set
from fixtures import graph

# Fix import statements in try block to run tests
try:
    from project.task4 import reachability_with_constraints
    from project.task2 import regex_to_dfa, graph_to_nfa
    from project.task3 import paths_ends, FiniteAutomaton
except ImportError:
    pytestmark = pytest.mark.skip("Task 4 is not ready to test!")


@pytest.fixture(scope="class", params=range(5))
def query(request) -> str:
    return random.choice(REGEXES)


class TestReachability:
    def test(self, graph, query) -> None:
        start_nodes, final_nodes = generate_rnd_start_and_final(graph.copy())
        fa = FiniteAutomaton(
            graph_to_nfa(deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes))
        )
        constraint_fa = FiniteAutomaton(regex_to_dfa(query))
        reachable = rpq_dict_to_set(
            reachability_with_constraints(deepcopy(fa), deepcopy(constraint_fa))
        )
        ends = paths_ends(
            deepcopy(graph), deepcopy(start_nodes), deepcopy(final_nodes), query
        )

        assert set(ends) == reachable
