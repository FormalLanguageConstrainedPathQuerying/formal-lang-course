# This file contains test cases that you need to pass to get a grade
# You MUST NOT touch anything here except ONE block below
# You CAN modify this file IF AND ONLY IF you have found a bug and are willing to fix it
# Otherwise, please report it
from copy import deepcopy
import pytest
from grammars_constants import REGEXP_CFG, GRAMMARS, GRAMMARS_DIFFERENT
from helper import generate_rnd_start_and_final
from rpq_template_test import rpq_cfpq_test, different_grammars_test
from fixtures import graph

# Fix import statements in try block to run tests
try:
    from project.task2 import graph_to_nfa, regex_to_dfa
    from project.task3 import FiniteAutomaton
    from project.task4 import reachability_with_constraints
    from project.task7 import cfpq_with_matrix
    from project.task6 import cfpq_with_hellings
except ImportError:
    pytestmark = pytest.mark.skip("Task 7 is not ready to test!")


class TestReachabilityMatrixAlgorithm:
    @pytest.mark.parametrize("regex_str, cfg_list", REGEXP_CFG)
    def test_rpq_cfpq_matrix(self, graph, regex_str, cfg_list) -> None:
        rpq_cfpq_test(graph, regex_str, cfg_list, cfpq_with_matrix)

    @pytest.mark.parametrize("eq_grammars", GRAMMARS)
    def test_different_grammars_matrix(self, graph, eq_grammars):
        different_grammars_test(graph, eq_grammars, cfpq_with_matrix)

    @pytest.mark.parametrize("grammar", GRAMMARS_DIFFERENT)
    def test_hellings_matrix(self, graph, grammar):
        start_nodes, final_nodes = generate_rnd_start_and_final(graph)
        hellings = cfpq_with_hellings(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        matrix = cfpq_with_matrix(
            deepcopy(grammar), deepcopy(graph), start_nodes, final_nodes
        )
        assert hellings == matrix
